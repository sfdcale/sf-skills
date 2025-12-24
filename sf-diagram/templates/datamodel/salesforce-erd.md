# Salesforce ERD Template

Entity Relationship Diagram template for visualizing Salesforce data models with object type indicators, LDV markers, OWD annotations, and relationship type labels.

## When to Use
- Documenting object relationships
- Planning data model changes
- Understanding existing schema
- Design reviews and architecture discussions

## Cloud-Specific Templates

For pre-built cloud diagrams, see:
- **[Sales Cloud ERD](sales-cloud-erd.md)** - Account, Contact, Opportunity, Lead, Product, Campaign
- **[Service Cloud ERD](service-cloud-erd.md)** - Case, Entitlement, Knowledge, ServiceContract

## ERD Conventions

See **[ERD Conventions](../../docs/erd-conventions.md)** for full documentation.

### Object Type Indicators

| Indicator | Type | Color (Flowchart) |
|-----------|------|-------------------|
| `[STD]` | Standard Object | Sky Blue `#bae6fd` |
| `[CUST]` | Custom Object | Orange `#fed7aa` |
| `[EXT]` | External Object | Green `#a7f3d0` |

### Relationship Type Labels

| Label | Type | Arrow (Flowchart) |
|-------|------|-------------------|
| `LK` | Lookup | `-->` |
| `MD` | Master-Detail | `==>` (thick) |

### Metadata Annotations

| Annotation | Source | Example |
|------------|--------|---------|
| `LDV[~4M]` | Record count >2M | Large Data Volume |
| `OWD:Private` | Sharing model | Org-Wide Default |

---

## Query Org Metadata

Enrich diagrams with live org data:

```bash
python3 ~/.claude/plugins/marketplaces/sf-skills/sf-diagram/scripts/query-org-metadata.py \
    --objects Account,Contact,Opportunity,Case \
    --target-org myorg \
    --output table \
    --mermaid
```

## sf-metadata Integration

When connected to an org, query object definitions:

```
Skill(skill="sf-metadata")
Request: "Describe objects: Account, Contact, Opportunity, Case"
```

This returns:
- Field names and types
- Lookup/Master-Detail relationships
- Required fields
- External IDs

## Mermaid Template - Standard Sales Cloud

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#bae6fd',
  'primaryTextColor': '#1f2937',
  'primaryBorderColor': '#0369a1',
  'lineColor': '#334155',
  'tertiaryColor': '#f8fafc'
}}}%%
erDiagram
    %% ═══════════════════════════════════════════════════════════════════════════
    %% LEGEND - Relationship Types:
    %%   LK = Lookup (optional parent, no cascade delete)
    %%   MD = Master-Detail (required parent, cascade delete)
    %% ═══════════════════════════════════════════════════════════════════════════

    Account ||--o{ Contact : "LK - has many"
    Account ||--o{ Opportunity : "LK - has many"
    Account ||--o{ Case : "LK - has many"
    Account ||--o{ Account : "LK - parent of"

    Account {
        Id Id PK "[STD] {{LDV}}"
        Text Name "Required"
        Lookup ParentId FK "Account (Self)"
        Lookup OwnerId FK "User"
        Picklist Industry
        Picklist Type
        Currency AnnualRevenue
        Phone Phone
        Text __metadata__ "{{OWD}}"
    }

    Contact {
        Id Id PK "[STD]"
        Lookup AccountId FK "Account"
        Lookup OwnerId FK "User"
        Lookup ReportsToId FK "Contact (Self)"
        Text FirstName
        Text LastName "Required"
        Email Email
        Phone Phone
        Text __metadata__ "{{OWD}}"
    }

    Opportunity ||--o{ OpportunityLineItem : "MD - contains"
    Opportunity ||--o{ OpportunityContactRole : "MD - involves"
    Contact ||--o{ OpportunityContactRole : "LK - plays role"

    Opportunity {
        Id Id PK "[STD] {{LDV}}"
        Lookup AccountId FK "Account"
        Lookup OwnerId FK "User"
        Text Name "Required"
        Picklist StageName "Required"
        Date CloseDate "Required"
        Currency Amount
        Number Probability
        Text __metadata__ "{{OWD}}"
    }

    OpportunityContactRole {
        Id Id PK "[STD]"
        MasterDetail OpportunityId FK "Opportunity"
        Lookup ContactId FK "Contact"
        Picklist Role
        Checkbox IsPrimary
    }

    Product2 ||--o{ PricebookEntry : "LK - priced in"
    Pricebook2 ||--o{ PricebookEntry : "MD - contains"
    PricebookEntry ||--o{ OpportunityLineItem : "LK - used in"

    Product2 {
        Id Id PK "[STD]"
        Text Name "Required"
        Text ProductCode
        Checkbox IsActive "Required"
    }

    Pricebook2 {
        Id Id PK "[STD]"
        Text Name "Required"
        Checkbox IsActive
        Checkbox IsStandard
    }

    PricebookEntry {
        Id Id PK "[STD]"
        Lookup Product2Id FK "Product2"
        MasterDetail Pricebook2Id FK "Pricebook2"
        Currency UnitPrice "Required"
    }

    OpportunityLineItem {
        Id Id PK "[STD]"
        MasterDetail OpportunityId FK "Opportunity"
        Lookup PricebookEntryId FK "PricebookEntry"
        Number Quantity "Required"
        Currency TotalPrice
    }

    Case {
        Id Id PK "[STD] {{LDV}}"
        Lookup AccountId FK "Account"
        Lookup ContactId FK "Contact"
        Lookup OwnerId FK "User, Queue"
        Lookup ParentId FK "Case (Self)"
        Text Subject
        Picklist Status "Required"
        Picklist Priority
        Picklist Origin
        Text __metadata__ "{{OWD}}"
    }

    User ||--o{ Account : "LK - owns"
    User ||--o{ Contact : "LK - owns"
    User ||--o{ Opportunity : "LK - owns"
    User ||--o{ Case : "LK - owns"

    User {
        Id Id PK "[STD]"
        Text Username "Required, Unique"
        Text LastName "Required"
        Email Email "Required"
        Checkbox IsActive
        Lookup ProfileId FK "Profile"
    }
```

## ASCII Fallback Template

```
┌─────────────────────────────┐
│          ACCOUNT            │
├─────────────────────────────┤
│ Id (PK)                     │
│ Name (Required)             │
│ ParentId (FK → Account)     │──────────────────┐
│ OwnerId (FK → User)         │                  │
│ Industry                    │                  │
│ Type                        │                  │
│ AnnualRevenue               │                  │
└─────────────┬───────────────┘                  │
              │                                   │
              │ 1:N                               │
              ▼                                   │
┌─────────────────────────────┐                  │
│          CONTACT            │                  │
├─────────────────────────────┤                  │
│ Id (PK)                     │                  │
│ AccountId (FK → Account) ───│──────────────────┘
│ OwnerId (FK → User)         │
│ ReportsToId (FK → Contact)  │───┐
│ FirstName                   │   │
│ LastName (Required)         │   │ Self-reference
│ Email                       │<──┘
│ Phone                       │
└─────────────────────────────┘

              │
              │ N:M (via junction)
              ▼

┌─────────────────────────────┐     ┌─────────────────────────────┐
│  OPPORTUNITY_CONTACT_ROLE   │     │        OPPORTUNITY          │
├─────────────────────────────┤     ├─────────────────────────────┤
│ Id (PK)                     │     │ Id (PK)                     │
│ OpportunityId (FK) ─────────│────>│ AccountId (FK → Account)    │
│ ContactId (FK → Contact)    │     │ OwnerId (FK → User)         │
│ Role                        │     │ Name (Required)             │
│ IsPrimary                   │     │ StageName (Required)        │
└─────────────────────────────┘     │ CloseDate (Required)        │
                                    │ Amount                      │
                                    └─────────────┬───────────────┘
                                                  │
                                                  │ 1:N
                                                  ▼
                                    ┌─────────────────────────────┐
                                    │    OPPORTUNITY_LINE_ITEM    │
                                    ├─────────────────────────────┤
                                    │ Id (PK)                     │
                                    │ OpportunityId (FK)          │
                                    │ PricebookEntryId (FK)       │
                                    │ Quantity (Required)         │
                                    │ UnitPrice                   │
                                    │ TotalPrice                  │
                                    └─────────────────────────────┘
```

## Cardinality Notation

| Symbol | Meaning | Salesforce Equivalent |
|--------|---------|----------------------|
| `\|\|` | Exactly one | Required Lookup |
| `\|o` | Zero or one | Optional Lookup |
| `o{` | Zero or many | Child objects |
| `\|{` | One or many | Required children |

## Relationship Types

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#a5f3fc',
  'primaryTextColor': '#1f2937',
  'primaryBorderColor': '#0e7490',
  'lineColor': '#334155',
  'tertiaryColor': '#f8fafc'
}}}%%
erDiagram
    %% Master-Detail (cascade delete)
    Parent ||--o{ Child_MasterDetail : "owns (MD)"

    %% Lookup (no cascade)
    Parent ||--o{ Child_Lookup : "references (LK)"

    %% Self-Referential
    Employee ||--o{ Employee : "manages"

    %% Junction Object (Many-to-Many)
    TableA ||--o{ Junction : "linked via"
    TableB ||--o{ Junction : "linked via"
```

## Salesforce Field Type Mapping

| Salesforce Type | ERD Type | Example |
|-----------------|----------|---------|
| Id | Id | `Id Id PK` |
| Text | Text | `Text Name` |
| Text Area | TextArea | `TextArea Description` |
| Number | Number | `Number Quantity` |
| Currency | Currency | `Currency Amount` |
| Percent | Percent | `Percent Probability` |
| Checkbox | Checkbox | `Checkbox IsActive` |
| Date | Date | `Date CloseDate` |
| DateTime | DateTime | `DateTime CreatedDate` |
| Picklist | Picklist | `Picklist Status` |
| Multi-Picklist | MultiPicklist | `MultiPicklist Industries` |
| Email | Email | `Email Email` |
| Phone | Phone | `Phone Phone` |
| URL | URL | `URL Website` |
| Lookup | Lookup | `Lookup AccountId FK "Account"` |
| Master-Detail | MasterDetail | `MasterDetail AccountId FK "Account"` |
| Formula | Formula | `Formula FullName` |
| Roll-Up Summary | RollUp | `RollUp TotalAmount` |

## Custom Object Example

Shows mixing Standard (blue) and Custom (orange) objects:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#bae6fd',
  'primaryTextColor': '#1f2937',
  'primaryBorderColor': '#0369a1',
  'lineColor': '#334155'
}}}%%
erDiagram
    Account ||--o{ Invoice__c : "MD - has many"
    Invoice__c ||--o{ Invoice_Line_Item__c : "MD - contains"
    Product2 ||--o{ Invoice_Line_Item__c : "LK - sold as"

    Invoice__c {
        Id Id PK "[CUST]"
        Text Name "Auto-Number"
        MasterDetail Account__c FK "Account"
        Lookup Contact__c FK "Contact"
        Date Invoice_Date__c "Required"
        Picklist Status__c "Draft/Sent/Paid"
        Currency Total_Amount__c "Roll-Up"
        Text __metadata__ "OWD:Private"
    }

    Invoice_Line_Item__c {
        Id Id PK "[CUST]"
        Text Name "Auto-Number"
        MasterDetail Invoice__c FK "Invoice__c"
        Lookup Product__c FK "Product2"
        Number Quantity__c "Required"
        Currency Unit_Price__c
        Formula Line_Total__c "Qty * Price"
    }
```

### Flowchart Version (With Colors)

```mermaid
%%{init: {"flowchart": {"nodeSpacing": 60, "rankSpacing": 50}} }%%
flowchart TB
    subgraph std["STANDARD OBJECTS"]
        Account["Account<br/>{{LDV}} | OWD:Private"]
        Product2["Product2"]
    end

    subgraph cust["CUSTOM OBJECTS"]
        Invoice["Invoice__c<br/>OWD:Private"]
        InvoiceLine["Invoice_Line_Item__c"]
    end

    Account ==>|"MD"| Invoice
    Invoice ==>|"MD"| InvoiceLine
    Product2 -->|"LK"| InvoiceLine

    %% Standard - Sky Blue
    style Account fill:#bae6fd,stroke:#0369a1,color:#1f2937
    style Product2 fill:#bae6fd,stroke:#0369a1,color:#1f2937

    %% Custom - Orange
    style Invoice fill:#fed7aa,stroke:#c2410c,color:#1f2937
    style InvoiceLine fill:#fed7aa,stroke:#c2410c,color:#1f2937

    %% Subgraphs
    style std fill:#f0f9ff,stroke:#0369a1,stroke-dasharray:5
    style cust fill:#fff7ed,stroke:#c2410c,stroke-dasharray:5
```

## Best Practices

1. **Use API Names** - Show `Account__c` not "Custom Account"
2. **Mark Required Fields** - Add "Required" notation
3. **Show Relationship Type** - MD vs Lookup distinction matters
4. **Include Key Fields Only** - Don't overcrowd; focus on relationships
5. **Group Related Objects** - Use visual proximity

## Generating from sf-metadata

When sf-metadata returns object info, map to ERD:

```javascript
// Example mapping
{
  "name": "Account",
  "fields": [
    { "name": "Id", "type": "id" },
    { "name": "Name", "type": "string", "nillable": false },
    { "name": "ParentId", "type": "reference", "referenceTo": ["Account"] }
  ]
}

// Becomes:
// Account {
//     Id Id PK
//     Text Name "Required"
//     Lookup ParentId FK "Account"
// }
```

## Customization Points

- Add custom objects by following the pattern
- Include only relevant fields (not all 200+ standard fields)
- Use comments `%% Comment` for notes
- Adjust layout by reordering entities
