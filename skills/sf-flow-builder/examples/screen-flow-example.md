# Screen Flow Example: Customer Feedback Form

This example demonstrates creating a Screen Flow that collects customer feedback and creates a custom object record.

## Scenario

Create an interactive form where users can:
- Select a product from a picklist
- Rate their experience (1-5 stars)
- Provide comments
- Submit feedback to a custom Feedback__c object

## User Request

```
User: "Create a screen flow for customer feedback collection.
It should have a welcome screen, collect product selection,
rating (1-5), and comments, then save to the Feedback__c object."
```

## Skill Workflow

### Phase 1: Requirements Gathering

The skill asks:

**Q1: What type of flow?**
→ Screen Flow

**Q2: What is the purpose?**
→ "Collect customer feedback and save to Feedback__c object"

**Q3: Target org?**
→ "sandbox" (or whatever org alias you provide)

### Phase 2: Flow Design

The skill designs:
- **Screen 1**: Welcome message
- **Screen 2**: Feedback form
  - Product picklist
  - Rating (1-5)
  - Comments text area
- **Create Record**: Save to Feedback__c
- **Screen 3**: Thank you confirmation

### Phase 3: Validation

```
Flow Validation Report: Customer_Feedback_Screen_Flow (API 62.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ XML Structure: Valid
✓ API Version: 62.0 (current - Winter '26)
✓ Required Elements: Present
✓ Element References: All valid
✓ Naming Conventions: Compliant

⚠ Warnings: None
✗ Errors: None

Best Practices Score: 100/100 (Excellent ✨)

✓ VALIDATION PASSED - Flow ready for deployment
```

### Phase 4: Deployment

**Step 1: Check-Only Validation**
```
Deploying flow with --check-only flag...
✓ Validation successful
✓ No org-specific errors
✓ Ready for actual deployment
```

**Step 2: Actual Deployment**
```
Deploying to sandbox...
✓ Deployment successful
Job ID: 0Af5g00000XXXXX
Flow deployed as Draft
```

**Step 3: Activation Prompt**
```
Would you like to activate the flow 'Customer_Feedback_Screen_Flow' now,
or keep it in Draft status?

Options:
- Activate Now
- Keep as Draft (recommended for testing first)

User selects: Keep as Draft
```

### Phase 5: Testing Checklist

```
✓ Testing Checklist: Customer_Feedback_Screen_Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Navigate to Setup → Flows → Customer_Feedback_Screen_Flow
□ Click "Run" to test UI in sandbox
□ Verify welcome screen displays correctly
□ Test product picklist shows all options
□ Verify rating field accepts 1-5
□ Enter test comments
□ Submit form
□ Check Feedback__c object for new record
□ Verify all fields populated correctly
□ Test with empty fields (validation)
□ Test with different products and ratings

Manual Test URL:
https://[your-sandbox].lightning.force.com/lightning/setup/Flows/page?address=%2F[FlowId]
```

## Generated Flow Structure

### Variables

```xml
<variables>
    <name>varProductName</name>
    <dataType>String</dataType>
    <isCollection>false</isCollection>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>

<variables>
    <name>varRating</name>
    <dataType>Number</dataType>
    <isCollection>false</isCollection>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
    <scale>0</scale>
</variables>

<variables>
    <name>varComments</name>
    <dataType>String</dataType>
    <isCollection>false</isCollection>
    <isInput>false</isInput>
    <isOutput>false</isOutput>
</variables>
```

### Screen Elements

**Welcome Screen**
- Display text with instructions
- Next button

**Feedback Form Screen**
- Picklist: Product selection → varProductName
- Number input: Rating (1-5) → varRating
- Long text area: Comments → varComments
- Previous/Next buttons

**Thank You Screen**
- Display text with confirmation
- Finish button

### Record Create

```xml
<recordCreates>
    <name>Create_Feedback_Record</name>
    <label>Create Feedback Record</label>
    <inputAssignments>
        <field>Product__c</field>
        <value>
            <elementReference>varProductName</elementReference>
        </value>
    </inputAssignments>
    <inputAssignments>
        <field>Rating__c</field>
        <value>
            <elementReference>varRating</elementReference>
        </value>
    </inputAssignments>
    <inputAssignments>
        <field>Comments__c</field>
        <value>
            <elementReference>varComments</elementReference>
        </value>
    </inputAssignments>
    <object>Feedback__c</object>
    <faultConnector>
        <targetReference>Error_Screen</targetReference>
    </faultConnector>
</recordCreates>
```

## Testing Results

### Manual Testing
1. ✓ Flow runs successfully
2. ✓ All screens display as expected
3. ✓ Form validation works correctly
4. ✓ Record created in Feedback__c
5. ✓ All field values mapped correctly

### Edge Cases Tested
- Empty product selection → validation message
- Rating outside 1-5 range → validation message
- Very long comments (>32,000 chars) → truncated
- Special characters in comments → handled correctly

## Production Deployment

After testing in sandbox:

1. Activate the flow:
   - Setup → Flows → Customer_Feedback_Screen_Flow → Activate

2. Add to Lightning page or Experience Cloud site

3. Deploy to production:
   ```
   "Deploy Customer_Feedback_Screen_Flow to production"
   ```

4. Monitor usage:
   - Check Debug Logs for any errors
   - Review submitted feedback records
   - Monitor for user-reported issues

## Enhancements

Possible improvements:
- Add email notification on submission
- Create dashboard to view feedback
- Add file upload for screenshots
- Implement duplicate checking
- Add confirmation email to submitter

## Key Takeaways

✓ Screen flows are perfect for guided user experiences
✓ Use meaningful variable names with type prefixes (var, col)
✓ Always test in sandbox before production
✓ Keep flows as Draft until thoroughly tested
✓ Add fault paths to DML operations
✓ Validate user input before processing
