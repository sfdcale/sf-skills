/**
 * @description Service class for {{ObjectName}} business logic
 * @author {{Author}}
 * @date {{Date}}
 */
public with sharing class {{ObjectName}}Service {

    private {{ObjectName}}Selector selector;

    /**
     * @description Default constructor
     */
    public {{ObjectName}}Service() {
        this.selector = new {{ObjectName}}Selector();
    }

    /**
     * @description Constructor with dependency injection
     * @param selector Selector instance for querying
     */
    @TestVisible
    private {{ObjectName}}Service({{ObjectName}}Selector selector) {
        this.selector = selector;
    }

    /**
     * @description Gets records by IDs
     * @param ids Set of record IDs
     * @return Map of records by ID
     */
    public Map<Id, {{ObjectName}}> getRecordsById(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) {
            return new Map<Id, {{ObjectName}}>();
        }

        List<{{ObjectName}}> records = selector.selectById(ids);
        return new Map<Id, {{ObjectName}}>(records);
    }

    /**
     * @description Creates new records
     * @param records List of records to create
     * @return List of created records with IDs
     */
    public List<{{ObjectName}}> createRecords(List<{{ObjectName}}> records) {
        if (records == null || records.isEmpty()) {
            return new List<{{ObjectName}}>();
        }

        // Apply defaults
        for ({{ObjectName}} record : records) {
            applyDefaults(record);
        }

        // Validate
        validateRecords(records);

        // Insert
        insert records;

        return records;
    }

    /**
     * @description Updates existing records
     * @param records List of records to update
     * @return List of updated records
     */
    public List<{{ObjectName}}> updateRecords(List<{{ObjectName}}> records) {
        if (records == null || records.isEmpty()) {
            return new List<{{ObjectName}}>();
        }

        // Validate
        validateRecords(records);

        // Update
        update records;

        return records;
    }

    /**
     * @description Deletes records
     * @param ids Set of record IDs to delete
     */
    public void deleteRecords(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) {
            return;
        }

        List<{{ObjectName}}> records = selector.selectById(ids);
        delete records;
    }

    /**
     * @description Applies default values to a record
     * @param record Record to apply defaults to
     */
    private void applyDefaults({{ObjectName}} record) {
        // TODO: Implement default logic
        // record.Status__c = record.Status__c ?? 'New';
    }

    /**
     * @description Validates records before DML
     * @param records Records to validate
     * @throws ValidationException if validation fails
     */
    private void validateRecords(List<{{ObjectName}}> records) {
        List<String> errors = new List<String>();

        for ({{ObjectName}} record : records) {
            if (String.isBlank(record.Name)) {
                errors.add('Name is required');
            }
            // TODO: Add more validation rules
        }

        if (!errors.isEmpty()) {
            throw new ValidationException(String.join(errors, '; '));
        }
    }

    /**
     * @description Custom exception for validation errors
     */
    public class ValidationException extends Exception {}
}
