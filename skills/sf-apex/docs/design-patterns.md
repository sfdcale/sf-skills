# Apex Design Patterns

## Factory Pattern

### Purpose
Centralize object creation, enable dependency injection, simplify testing.

### Implementation

```apex
public virtual class Factory {
    private static Factory instance;

    public static Factory getInstance() {
        if (instance == null) {
            instance = new Factory();
        }
        return instance;
    }

    @TestVisible
    private static void setInstance(Factory mockFactory) {
        instance = mockFactory;
    }

    // Service getters - virtual for mocking
    public virtual AccountService getAccountService() {
        return new AccountService();
    }

    public virtual ContactService getContactService() {
        return new ContactService();
    }

    public virtual PaymentGateway getPaymentGateway() {
        return new StripePaymentGateway();
    }
}
```

### Usage

```apex
public class OrderProcessor {
    private AccountService accountService;
    private PaymentGateway gateway;

    public OrderProcessor() {
        this(Factory.getInstance());
    }

    @TestVisible
    private OrderProcessor(Factory factory) {
        this.accountService = factory.getAccountService();
        this.gateway = factory.getPaymentGateway();
    }

    public void process(Order__c order) {
        Account acc = accountService.getAccount(order.Account__c);
        gateway.charge(order.Total__c);
    }
}
```

### Testing with Factory

```apex
@isTest
private class OrderProcessorTest {

    @isTest
    static void testProcess() {
        // Set mock factory
        Factory.setInstance(new MockFactory());

        OrderProcessor processor = new OrderProcessor();

        Test.startTest();
        processor.process(new Order__c());
        Test.stopTest();

        // Assertions
    }

    private class MockFactory extends Factory {
        public override AccountService getAccountService() {
            return new MockAccountService();
        }

        public override PaymentGateway getPaymentGateway() {
            return new MockPaymentGateway();
        }
    }
}
```

---

## Repository Pattern

### Purpose
Abstract data access, provide strongly-typed queries, enable DML mocking.

### Implementation

```apex
public virtual class AccountRepository {

    public virtual List<Account> getByIds(Set<Id> accountIds) {
        return [
            SELECT Id, Name, Industry, AnnualRevenue
            FROM Account
            WHERE Id IN :accountIds
            WITH USER_MODE
        ];
    }

    public virtual List<Account> getByIndustry(String industry) {
        return [
            SELECT Id, Name, AnnualRevenue
            FROM Account
            WHERE Industry = :industry
            WITH USER_MODE
        ];
    }

    public virtual Account getById(Id accountId) {
        List<Account> accounts = getByIds(new Set<Id>{accountId});
        return accounts.isEmpty() ? null : accounts[0];
    }

    public virtual void save(List<Account> accounts) {
        upsert accounts;
    }

    public virtual void remove(List<Account> accounts) {
        delete accounts;
    }
}
```

### Usage

```apex
public class AccountService {
    private AccountRepository repo;

    public AccountService() {
        this.repo = new AccountRepository();
    }

    @TestVisible
    private AccountService(AccountRepository repo) {
        this.repo = repo;
    }

    public List<Account> getTechnologyAccounts() {
        return repo.getByIndustry('Technology');
    }

    public void updateAccounts(List<Account> accounts) {
        repo.save(accounts);
    }
}
```

### Testing with Mock Repository

```apex
@isTest
private class AccountServiceTest {

    @isTest
    static void testGetTechnologyAccounts() {
        MockAccountRepository mockRepo = new MockAccountRepository();
        mockRepo.accountsToReturn = new List<Account>{
            new Account(Name = 'Test', Industry = 'Technology')
        };

        AccountService service = new AccountService(mockRepo);

        Test.startTest();
        List<Account> results = service.getTechnologyAccounts();
        Test.stopTest();

        Assert.areEqual(1, results.size());
        Assert.areEqual('Technology', mockRepo.lastIndustryQueried);
    }

    private class MockAccountRepository extends AccountRepository {
        public List<Account> accountsToReturn = new List<Account>();
        public String lastIndustryQueried;

        public override List<Account> getByIndustry(String industry) {
            this.lastIndustryQueried = industry;
            return accountsToReturn;
        }
    }
}
```

---

## Selector Pattern

### Purpose
Centralize SOQL queries per object, enforce security, enable reuse.

### Implementation

```apex
public inherited sharing class AccountSelector {

    public List<Account> selectById(Set<Id> ids) {
        return [
            SELECT Id, Name, Industry, AnnualRevenue, BillingCity
            FROM Account
            WHERE Id IN :ids
            WITH USER_MODE
        ];
    }

    public List<Account> selectByIdWithContacts(Set<Id> ids) {
        return [
            SELECT Id, Name, Industry,
                (SELECT Id, FirstName, LastName, Email FROM Contacts)
            FROM Account
            WHERE Id IN :ids
            WITH USER_MODE
        ];
    }

    public List<Account> selectByName(String name) {
        return [
            SELECT Id, Name, Industry
            FROM Account
            WHERE Name LIKE :('%' + name + '%')
            WITH USER_MODE
            LIMIT 100
        ];
    }

    public List<Account> selectActiveByIndustry(String industry) {
        return [
            SELECT Id, Name, AnnualRevenue
            FROM Account
            WHERE Industry = :industry
            AND Status__c = 'Active'
            WITH USER_MODE
        ];
    }
}
```

### Usage

```apex
public class AccountService {
    private AccountSelector selector = new AccountSelector();

    public Map<Id, Account> getAccountsMap(Set<Id> ids) {
        return new Map<Id, Account>(selector.selectById(ids));
    }
}
```

---

## Builder Pattern

### Purpose
Construct complex objects step-by-step, improve readability.

### Implementation

```apex
public class AccountBuilder {
    private Account record;

    public AccountBuilder() {
        this.record = new Account();
    }

    public AccountBuilder withName(String name) {
        this.record.Name = name;
        return this;
    }

    public AccountBuilder withIndustry(String industry) {
        this.record.Industry = industry;
        return this;
    }

    public AccountBuilder withAnnualRevenue(Decimal revenue) {
        this.record.AnnualRevenue = revenue;
        return this;
    }

    public AccountBuilder withBillingAddress(String city, String state, String country) {
        this.record.BillingCity = city;
        this.record.BillingState = state;
        this.record.BillingCountry = country;
        return this;
    }

    public AccountBuilder withParent(Id parentId) {
        this.record.ParentId = parentId;
        return this;
    }

    public Account build() {
        return this.record;
    }

    public Account buildAndInsert() {
        insert this.record;
        return this.record;
    }
}
```

### Usage

```apex
// Fluent interface for building objects
Account acc = new AccountBuilder()
    .withName('Acme Corporation')
    .withIndustry('Technology')
    .withAnnualRevenue(1000000)
    .withBillingAddress('San Francisco', 'CA', 'USA')
    .buildAndInsert();

// In tests
Account testAccount = new AccountBuilder()
    .withName('Test Account')
    .build();  // Don't insert for unit tests
```

---

## Singleton Pattern

### Purpose
Ensure single instance, cache expensive operations.

### Implementation

```apex
public class ConfigurationService {
    private static ConfigurationService instance;
    private Map<String, String> settings;

    private ConfigurationService() {
        // Load settings once
        this.settings = new Map<String, String>();
        for (Configuration__mdt config : [SELECT DeveloperName, Value__c FROM Configuration__mdt]) {
            settings.put(config.DeveloperName, config.Value__c);
        }
    }

    public static ConfigurationService getInstance() {
        if (instance == null) {
            instance = new ConfigurationService();
        }
        return instance;
    }

    public String getSetting(String key) {
        return settings.get(key);
    }

    public String getSetting(String key, String defaultValue) {
        return settings.containsKey(key) ? settings.get(key) : defaultValue;
    }

    // For testing
    @TestVisible
    private static void reset() {
        instance = null;
    }
}
```

### Usage

```apex
String apiUrl = ConfigurationService.getInstance().getSetting('API_URL');
String timeout = ConfigurationService.getInstance().getSetting('TIMEOUT', '30000');
```

---

## Strategy Pattern

### Purpose
Define family of algorithms, make them interchangeable.

### Implementation

```apex
public interface DiscountStrategy {
    Decimal calculate(Decimal amount);
    String getDescription();
}

public class PercentageDiscount implements DiscountStrategy {
    private Decimal percentage;

    public PercentageDiscount(Decimal percentage) {
        this.percentage = percentage;
    }

    public Decimal calculate(Decimal amount) {
        return amount * (percentage / 100);
    }

    public String getDescription() {
        return percentage + '% off';
    }
}

public class FixedAmountDiscount implements DiscountStrategy {
    private Decimal fixedAmount;

    public FixedAmountDiscount(Decimal amount) {
        this.fixedAmount = amount;
    }

    public Decimal calculate(Decimal amount) {
        return Math.min(fixedAmount, amount);
    }

    public String getDescription() {
        return '$' + fixedAmount + ' off';
    }
}

public class TieredDiscount implements DiscountStrategy {
    public Decimal calculate(Decimal amount) {
        if (amount > 1000) return amount * 0.15;
        if (amount > 500) return amount * 0.10;
        if (amount > 100) return amount * 0.05;
        return 0;
    }

    public String getDescription() {
        return 'Tiered discount based on amount';
    }
}
```

### Usage

```apex
public class PricingService {
    private Map<String, DiscountStrategy> strategies;

    public PricingService() {
        strategies = new Map<String, DiscountStrategy>{
            'PERCENTAGE_10' => new PercentageDiscount(10),
            'FIXED_50' => new FixedAmountDiscount(50),
            'TIERED' => new TieredDiscount()
        };
    }

    public Decimal applyDiscount(String discountType, Decimal amount) {
        DiscountStrategy strategy = strategies.get(discountType);
        if (strategy == null) {
            return 0;
        }
        return strategy.calculate(amount);
    }
}
```

---

## Unit of Work Pattern

### Purpose
Manage DML as single transaction, track changes, enable rollback.

### Basic Implementation

```apex
public class UnitOfWork {
    private List<SObject> newRecords = new List<SObject>();
    private List<SObject> dirtyRecords = new List<SObject>();
    private List<SObject> deletedRecords = new List<SObject>();

    public void registerNew(SObject record) {
        newRecords.add(record);
    }

    public void registerNew(List<SObject> records) {
        newRecords.addAll(records);
    }

    public void registerDirty(SObject record) {
        dirtyRecords.add(record);
    }

    public void registerDeleted(SObject record) {
        deletedRecords.add(record);
    }

    public void commitWork() {
        Savepoint sp = Database.setSavepoint();
        try {
            insert newRecords;
            update dirtyRecords;
            delete deletedRecords;
        } catch (Exception e) {
            Database.rollback(sp);
            throw e;
        }
    }
}
```

### Usage

```apex
public class OrderService {
    public void processOrder(Order__c order, List<OrderItem__c> items) {
        UnitOfWork uow = new UnitOfWork();

        // Register all changes
        uow.registerNew(order);
        uow.registerNew(items);

        Account acc = [SELECT Id, Order_Count__c FROM Account WHERE Id = :order.Account__c];
        acc.Order_Count__c = (acc.Order_Count__c ?? 0) + 1;
        uow.registerDirty(acc);

        // Single commit - all or nothing
        uow.commitWork();
    }
}
```

---

## Pattern Selection Guide

| Need | Pattern |
|------|---------|
| Centralize object creation | Factory |
| Abstract data access | Repository / Selector |
| Build complex objects | Builder |
| Single cached instance | Singleton |
| Interchangeable algorithms | Strategy |
| Transactional DML | Unit of Work |
