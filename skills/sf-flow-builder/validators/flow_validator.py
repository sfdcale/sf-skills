#!/usr/bin/env python3
"""
Salesforce Flow Validator with Enhanced Scoring

Performs comprehensive validation of Salesforce Flow metadata XML files.
Enforces best practices, bulkification, and API standards.

Usage:
    python3 flow_validator.py <path-to-flow-meta.xml>
"""

import sys
import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict
import re

class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.recommendations: List[str] = []
        self.auto_fixes: List[Dict] = []
        self.score = 100

class FlowValidator:
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.tree = None
        self.root = None
        self.result = ValidationResult()
        self.namespace = {'ns': 'http://soap.sforce.com/2006/04/metadata'}

    def validate(self) -> ValidationResult:
        """Main validation entry point"""
        # Load and parse XML
        if not self._load_xml():
            return self.result

        # Run all validation checks
        self._check_xml_structure()
        self._check_api_version()
        self._check_required_elements()
        self._check_element_references()
        self._check_naming_conventions()
        self._check_bulkification()
        self._check_transform_usage()
        self._check_fault_paths()
        self._check_unused_elements()
        self._check_best_practices()

        return self.result

    def _load_xml(self) -> bool:
        """Load and parse XML file"""
        try:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            self.result.errors.append(f"❌ XML parse error: {str(e)}")
            self.result.score = 0
            return False
        except FileNotFoundError:
            self.result.errors.append(f"❌ File not found: {self.xml_path}")
            self.result.score = 0
            return False

    def _check_xml_structure(self):
        """Validate XML is well-formed"""
        if self.root.tag != '{http://soap.sforce.com/2006/04/metadata}Flow':
            self.result.errors.append("❌ Root element must be <Flow>")
            self.result.score -= 50

    def _check_api_version(self):
        """Check API version is 62.0 or higher"""
        api_elem = self.root.find('ns:apiVersion', self.namespace)
        if api_elem is None:
            self.result.errors.append("❌ Missing required element: apiVersion")
            self.result.score -= 50
            return

        try:
            version = float(api_elem.text)
            if version < 62.0:
                self.result.warnings.append(
                    f"⚠️  API version {version} is outdated. "
                    "Recommend 62.0 (Winter '26) for latest features (-10 pts)"
                )
                self.result.score -= 10
                self.result.recommendations.append(
                    "⬆️  Update to API 62.0 for Transform element and bulk support"
                )
        except ValueError:
            self.result.errors.append(f"❌ Invalid API version format: {api_elem.text}")
            self.result.score -= 50

    def _check_required_elements(self):
        """Check required Flow elements are present"""
        required = ['label', 'processType', 'status']
        for elem_name in required:
            elem = self.root.find(f'ns:{elem_name}', self.namespace)
            if elem is None:
                self.result.errors.append(f"❌ Missing required element: {elem_name}")
                self.result.score -= 50

    def _check_element_references(self):
        """Validate all connector references point to valid elements"""
        # Get all element names
        element_names = set()
        for elem in self.root:
            name_elem = elem.find('ns:name', self.namespace)
            if name_elem is not None:
                element_names.add(name_elem.text)

        # Check all connectors
        for connector in self.root.findall('.//ns:connector', self.namespace):
            target_ref = connector.find('ns:targetReference', self.namespace)
            if target_ref is not None and target_ref.text:
                if target_ref.text not in element_names:
                    self.result.errors.append(
                        f"❌ Broken reference: connector points to non-existent element '{target_ref.text}'"
                    )
                    self.result.score -= 50

    def _check_naming_conventions(self):
        """Check variable and element naming conventions"""
        # Check variables (should be camelCase with type prefix)
        for var in self.root.findall('ns:variables', self.namespace):
            name_elem = var.find('ns:name', self.namespace)
            if name_elem is not None:
                var_name = name_elem.text
                if not self._is_camel_case(var_name):
                    self.result.warnings.append(
                        f"⚠️  Variable '{var_name}' should use camelCase (-5 pts)"
                    )
                    self.result.score -= 5

                # Check type prefix
                if not (var_name.startswith('var') or var_name.startswith('col')):
                    self.result.recommendations.append(
                        f"💡 Consider prefixing variable '{var_name}' with type "
                        "(var for single, col for collection)"
                    )

        # Check elements (should use PascalCase with underscores)
        element_types = ['decisions', 'assignments', 'recordCreates',
                        'recordUpdates', 'recordDeletes', 'loops', 'screens']
        for elem_type in element_types:
            for elem in self.root.findall(f'ns:{elem_type}', self.namespace):
                name_elem = elem.find('ns:name', self.namespace)
                if name_elem is not None:
                    elem_name = name_elem.text
                    if not self._is_pascal_case_with_underscores(elem_name):
                        self.result.warnings.append(
                            f"⚠️  Element '{elem_name}' should use PascalCase_With_Underscores (-5 pts)"
                        )
                        self.result.score -= 5

    def _check_bulkification(self):
        """CRITICAL: Check for DML operations inside loops"""
        # Find all loops
        loops = self.root.findall('.//ns:loops', self.namespace)

        for loop in loops:
            loop_name = loop.find('ns:name', self.namespace).text

            # Check if loop has nextValueConnector
            next_connector = loop.find('ns:nextValueConnector', self.namespace)
            if next_connector is not None:
                target_ref = next_connector.find('ns:targetReference', self.namespace)
                if target_ref is not None:
                    # Follow the chain from this element
                    if self._has_dml_in_path(target_ref.text, loop_name):
                        self.result.errors.append(
                            f"❌ CRITICAL: DML operation inside loop '{loop_name}' "
                            "- will cause governor limit failures with bulk data (-50 pts)"
                        )
                        self.result.score -= 50
                        self.result.recommendations.append(
                            "🔧 Fix: Collect records in collection variable inside loop, "
                            "move DML outside loop to process entire collection at once"
                        )
                        self.result.auto_fixes.append({
                            'description': 'Restructure to move DML outside loop',
                            'element': loop_name
                        })

        # Check for bulkSupport attribute in record-triggered flows
        start_elem = self.root.find('ns:start', self.namespace)
        if start_elem is not None:
            trigger_type = start_elem.find('ns:triggerType', self.namespace)
            if trigger_type is not None:
                # This is a record-triggered flow
                bulk_support = start_elem.find('ns:bulkSupport', self.namespace)
                if bulk_support is None or bulk_support.text.lower() != 'true':
                    self.result.warnings.append(
                        "⚠️  Record-triggered flow missing <bulkSupport>true</bulkSupport> (-10 pts)"
                    )
                    self.result.score -= 10
                    self.result.auto_fixes.append({
                        'description': 'Add <bulkSupport>true</bulkSupport> to start element',
                        'element': 'start'
                    })

    def _check_transform_usage(self):
        """Check if loops could be replaced with Transform element"""
        loops = self.root.findall('.//ns:loops', self.namespace)

        for loop in loops:
            loop_name = loop.find('ns:name', self.namespace).text

            # Check if loop contains assignments (field mapping pattern)
            assignments_in_loop = self._find_assignments_in_loop_path(loop)
            if assignments_in_loop:
                self.result.warnings.append(
                    f"⚠️  Loop '{loop_name}' with field mapping detected - "
                    "consider using Transform element for 30-50% performance gain (-10 pts)"
                )
                self.result.score -= 10
                self.result.recommendations.append(
                    f"⚡ Replace loop '{loop_name}' with Transform element "
                    "[Learn more: https://help.salesforce.com/s/articleView?id=sf.flow_ref_elements_data_transform.htm]"
                )

    def _check_fault_paths(self):
        """Check DML operations have fault paths"""
        dml_types = ['recordCreates', 'recordUpdates', 'recordDeletes']

        for dml_type in dml_types:
            for dml_elem in self.root.findall(f'ns:{dml_type}', self.namespace):
                name_elem = dml_elem.find('ns:name', self.namespace)
                fault_connector = dml_elem.find('ns:faultConnector', self.namespace)

                if fault_connector is None:
                    dml_name = name_elem.text if name_elem is not None else 'Unknown'
                    self.result.warnings.append(
                        f"⚠️  DML operation '{dml_name}' missing fault path for error handling (-10 pts)"
                    )
                    self.result.score -= 10
                    self.result.auto_fixes.append({
                        'description': f"Add fault path to '{dml_name}'",
                        'element': dml_name
                    })

    def _check_unused_elements(self):
        """Check for unused variables and orphaned elements"""
        # Get all variable names
        all_vars = set()
        for var in self.root.findall('ns:variables', self.namespace):
            name_elem = var.find('ns:name', self.namespace)
            if name_elem is not None:
                all_vars.add(name_elem.text)

        # Get all variable references
        used_vars = set()
        for ref in self.root.findall('.//*[@elementReference]'):
            used_vars.add(ref.text)
        for ref in self.root.findall('.//ns:elementReference', self.namespace):
            used_vars.add(ref.text)

        # Find unused variables
        unused = all_vars - used_vars
        for var_name in unused:
            self.result.warnings.append(
                f"⚠️  Variable '{var_name}' declared but never used (-5 pts)"
            )
            self.result.score -= 5
            self.result.auto_fixes.append({
                'description': f"Remove unused variable '{var_name}'",
                'element': var_name
            })

    def _check_best_practices(self):
        """Check Salesforce Flow best practices"""
        # Check for flow description
        desc_elem = self.root.find('ns:description', self.namespace)
        if desc_elem is None or not desc_elem.text:
            self.result.recommendations.append(
                "📝 Add flow description for better documentation"
            )

        # Check status
        status_elem = self.root.find('ns:status', self.namespace)
        if status_elem is not None and status_elem.text == 'Active':
            self.result.recommendations.append(
                "⚠️  Flow is set to Active - ensure thorough testing before production deployment"
            )

    # Helper methods

    def _is_camel_case(self, name: str) -> bool:
        """Check if string is camelCase"""
        return bool(re.match(r'^[a-z][a-zA-Z0-9]*$', name))

    def _is_pascal_case_with_underscores(self, name: str) -> bool:
        """Check if string is PascalCase_With_Underscores"""
        return bool(re.match(r'^[A-Z][a-zA-Z0-9_]*$', name))

    def _has_dml_in_path(self, element_name: str, loop_name: str, visited=None) -> bool:
        """Check if path from element contains DML (used for loop checking)"""
        if visited is None:
            visited = set()

        if element_name in visited or element_name == loop_name:
            return False

        visited.add(element_name)

        # Find the element
        for elem_type in ['recordCreates', 'recordUpdates', 'recordDeletes']:
            elem = self._find_element_by_name(element_name, elem_type)
            if elem is not None:
                return True  # Found DML operation

        # Check other element types and follow connectors
        for elem_type in ['assignments', 'decisions', 'loops', 'screens']:
            elem = self._find_element_by_name(element_name, elem_type)
            if elem is not None:
                # Follow connectors
                for connector in elem.findall('.//ns:connector', self.namespace):
                    target_ref = connector.find('ns:targetReference', self.namespace)
                    if target_ref is not None:
                        if self._has_dml_in_path(target_ref.text, loop_name, visited):
                            return True

        return False

    def _find_element_by_name(self, name: str, elem_type: str):
        """Find element by name and type"""
        for elem in self.root.findall(f'ns:{elem_type}', self.namespace):
            name_elem = elem.find('ns:name', self.namespace)
            if name_elem is not None and name_elem.text == name:
                return elem
        return None

    def _find_assignments_in_loop_path(self, loop_elem) -> bool:
        """Check if loop path contains assignment operations (field mapping pattern)"""
        next_connector = loop_elem.find('ns:nextValueConnector', self.namespace)
        if next_connector is not None:
            target_ref = next_connector.find('ns:targetReference', self.namespace)
            if target_ref is not None:
                # Look for assignments in the path
                elem = self._find_element_by_name(target_ref.text, 'assignments')
                return elem is not None
        return False

def print_report(result: ValidationResult, flow_name: str):
    """Print formatted validation report"""
    print("━" * 60)
    print(f"Flow Validation Report: {flow_name} (API 62.0)")
    print("━" * 60)
    print()

    # Checkmarks for passed checks
    if not result.errors:
        print("✓ XML Structure: Valid")
        print("✓ Required Elements: Present")
        print("✓ Element References: All valid")

    # Errors
    if result.errors:
        print(f"\n✗ Errors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  {error}")
    else:
        print("\n✗ Errors: None")

    # Warnings
    if result.warnings:
        print(f"\n⚠  Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  {warning}")
    else:
        print("\n⚠  Warnings: None")

    # Score
    print(f"\n Best Practices Score: {result.score}/100", end="")
    if result.score >= 90:
        print(" (Excellent ✨)")
    elif result.score >= 75:
        print(" (Good - needs improvement)")
    elif result.score >= 50:
        print(" (Fair - significant issues)")
    else:
        print(" (Poor - critical issues)")

    # Auto-fixes
    if result.auto_fixes:
        print(f"\nAuto-Fix Available:")
        for i, fix in enumerate(result.auto_fixes, 1):
            print(f"  [{i}] {fix['description']}")

    # Recommendations
    if result.recommendations:
        print(f"\nRecommendations:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"  {i}. {rec}")

    print("\n" + "━" * 60)

    # Overall status
    if result.errors:
        print("❌ VALIDATION FAILED - Fix errors before deployment")
        return 1
    elif result.warnings:
        print("⚠️  VALIDATION PASSED WITH WARNINGS - Review warnings before deployment")
        return 0
    else:
        print("✓ VALIDATION PASSED - Flow ready for deployment")
        return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 flow_validator.py <path-to-flow-meta.xml>")
        sys.exit(1)

    xml_path = sys.argv[1]
    flow_name = xml_path.split('/')[-1].replace('.flow-meta.xml', '')

    validator = FlowValidator(xml_path)
    result = validator.validate()

    exit_code = print_report(result, flow_name)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
