# Lightning Web Components Best Practices

This guide provides comprehensive best practices for building production-ready LWC components, organized around the **PICKLES Framework** and incorporating advanced patterns from industry experts.

---

## PICKLES Framework Overview

The PICKLES Framework provides a structured approach to LWC architecture. Use it as a checklist during component design and implementation.

```
🥒 P - Prototype    → Validate ideas with wireframes & mock data
🥒 I - Integrate    → Choose data source (LDS, Apex, GraphQL)
🥒 C - Composition  → Structure component hierarchy & communication
🥒 K - Kinetics     → Handle user interactions & event flow
🥒 L - Libraries    → Leverage platform APIs & base components
🥒 E - Execution    → Optimize performance & lifecycle hooks
🥒 S - Security     → Enforce permissions & data protection
```

**Reference**: [PICKLES Framework (Salesforce Ben)](https://www.salesforceben.com/the-ideal-framework-for-architecting-salesforce-lightning-web-components/)

---

## Component Design Principles

### Single Responsibility (PICKLES: Composition)

Each component should do one thing well.

```
✅ GOOD: accountCard, accountList, accountForm (separate components)
❌ BAD: accountManager (does display, list, and form in one)
```

### Composition Over Inheritance

Build complex UIs by composing simple components.

```html
<!-- Compose components -->
<template>
    <c-page-header title="Accounts"></c-page-header>
    <c-account-filters onfilter={handleFilter}></c-account-filters>
    <c-account-list accounts={filteredAccounts}></c-account-list>
    <c-pagination total={totalCount} onpage={handlePage}></c-pagination>
</template>
```

### Unidirectional Data Flow

Data flows down (props), events bubble up.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA FLOW PATTERN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Parent Component                                               │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  state: accounts = [...]                                │   │
│   │                                                          │   │
│   │  ┌──────────┐     ┌──────────┐     ┌──────────┐        │   │
│   │  │ Child A  │ ←── │ Child B  │ ←── │ Child C  │        │   │
│   │  │          │     │          │     │          │        │   │
│   │  │ @api     │     │ @api     │     │ @api     │        │   │
│   │  │ accounts │     │ selected │     │ details  │        │   │
│   │  └────┬─────┘     └────┬─────┘     └────┬─────┘        │   │
│   │       │                │                │               │   │
│   │       │   Events       │   Events       │   Events      │   │
│   │       └────────────────┴────────────────┘               │   │
│   │              ↑ bubbles to parent                        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Integration (PICKLES: Integrate)

### Data Source Decision Tree

| Scenario | Recommended Approach |
|----------|---------------------|
| Single record by ID | Lightning Data Service (`getRecord`) |
| Simple record CRUD | `lightning-record-form` / `lightning-record-edit-form` |
| Complex queries | Apex with `@AuraEnabled(cacheable=true)` |
| Related records, filtering | GraphQL wire adapter |
| Real-time updates | Platform Events / Streaming API |
| External data | Named Credentials + Apex callout |

### GraphQL vs Apex Decision

| Use GraphQL When | Use Apex When |
|------------------|---------------|
| Fetching related objects | Complex business logic |
| Client-side filtering | Aggregate queries (COUNT, SUM) |
| Cursor-based pagination | Bulk DML operations |
| Reducing over-fetching | Callouts to external systems |

### Wire Service Best Practices

```javascript
// Store wire result for refreshApex
wiredAccountsResult;

@wire(getAccounts, { searchTerm: '$searchTerm' })
wiredAccounts(result) {
    this.wiredAccountsResult = result;  // Store for refresh
    const { data, error } = result;
    if (data) {
        this.accounts = data;
        this.error = undefined;
    } else if (error) {
        this.error = this.reduceErrors(error);
        this.accounts = [];
    }
}

// Refresh when needed
async handleRefresh() {
    await refreshApex(this.wiredAccountsResult);
}
```

### Error Handling Pattern

```javascript
// Centralized error reducer
reduceErrors(errors) {
    if (!Array.isArray(errors)) {
        errors = [errors];
    }

    return errors
        .filter(error => !!error)
        .map(error => {
            // UI API errors
            if (error.body?.message) return error.body.message;
            // JS errors
            if (error.message) return error.message;
            // GraphQL errors
            if (error.graphQLErrors) {
                return error.graphQLErrors.map(e => e.message).join(', ');
            }
            return JSON.stringify(error);
        })
        .join('; ');
}
```

---

## Event Patterns (PICKLES: Kinetics)

### Custom Events

```javascript
// Child dispatches event
this.dispatchEvent(new CustomEvent('select', {
    detail: { recordId: this.recordId },
    bubbles: true,    // Bubbles through DOM
    composed: true    // Crosses shadow boundary
}));

// Parent handles event
handleSelect(event) {
    const recordId = event.detail.recordId;
}
```

### Event Naming Conventions

```
✅ GOOD                    ❌ BAD
────────────────────────   ────────────────────────
onselect                   onSelectItem
onrecordchange             on-record-change
onsave                     onSaveClicked
onerror                    onErrorOccurred
```

### When to Use LMS vs Events

| Scenario | Use |
|----------|-----|
| Parent-child communication | Custom events |
| Sibling components (same parent) | Events via parent |
| Components on different parts of page | Lightning Message Service |
| LWC to Aura communication | LMS |
| LWC to Visualforce | LMS |

### Debouncing Pattern

```javascript
delayTimeout;

handleSearch(event) {
    const searchTerm = event.target.value;
    clearTimeout(this.delayTimeout);

    this.delayTimeout = setTimeout(() => {
        this.searchTerm = searchTerm;
    }, 300);  // 300ms debounce
}
```

---

## Performance Optimization (PICKLES: Execution)

### Lifecycle Hook Guidance

| Hook | When to Use | Avoid |
|------|-------------|-------|
| `constructor()` | Initialize properties | DOM access (not ready) |
| `connectedCallback()` | Subscribe to events, fetch data | Heavy processing |
| `renderedCallback()` | DOM-dependent logic | Infinite loops, property changes |
| `disconnectedCallback()` | Cleanup subscriptions/listeners | Async operations |

### Lazy Loading

```html
<!-- Only render when needed -->
<template lwc:if={showDetails}>
    <c-expensive-component record-id={recordId}></c-expensive-component>
</template>
```

### Efficient Rendering

```javascript
// Bad: Creates new array every render
get filteredItems() {
    return this.items.filter(item => item.active);
}

// Good: Cache the result
_filteredItems;
_itemsHash;

get filteredItems() {
    const currentHash = JSON.stringify(this.items);
    if (currentHash !== this._itemsHash) {
        this._filteredItems = this.items.filter(item => item.active);
        this._itemsHash = currentHash;
    }
    return this._filteredItems;
}
```

### Virtual Scrolling

Use `lightning-datatable` with `enable-infinite-loading` for large datasets instead of rendering all items.

---

## Advanced Jest Testing Patterns

Based on [James Simone's advanced testing patterns](https://www.jamessimone.net/blog/joys-of-apex/advanced-lwc-jest-testing/).

### Render Cycle Helper

LWC re-rendering is asynchronous. Use this helper to document and await render cycles:

```javascript
// testUtils.js
export const runRenderingLifecycle = async (reasons = ['render']) => {
    while (reasons.length > 0) {
        await Promise.resolve(reasons.pop());
    }
};

// Usage in tests
it('updates after property change', async () => {
    const element = createElement('c-example', { is: Example });
    document.body.appendChild(element);

    element.greeting = 'new value';
    await runRenderingLifecycle(['property change', 'render']);

    expect(element.shadowRoot.querySelector('div').textContent).toBe('new value');
});
```

### Proxy Unboxing (Lightning Web Security)

Lightning Web Security proxifies objects. Unbox them for assertions:

```javascript
// LWS proxifies complex objects - unbox for comparison
const unboxedData = JSON.parse(JSON.stringify(component.data));
expect(unboxedData).toEqual(expectedData);
```

### DOM Cleanup Pattern

Clean up after each test to prevent state bleed:

```javascript
describe('c-my-component', () => {
    afterEach(() => {
        // Clean up DOM
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });
});
```

### ResizeObserver Polyfill

Some components use ResizeObserver. Add polyfill in jest.setup.js:

```javascript
// jest.setup.js
if (!window.ResizeObserver) {
    window.ResizeObserver = class ResizeObserver {
        constructor(callback) {
            this.callback = callback;
        }
        observe() {}
        unobserve() {}
        disconnect() {}
    };
}
```

### Mocking Apex Methods

```javascript
jest.mock('@salesforce/apex/MyController.getData', () => ({
    default: jest.fn()
}), { virtual: true });

// In test
import getData from '@salesforce/apex/MyController.getData';

it('displays data', async () => {
    getData.mockResolvedValue(MOCK_DATA);
    // ... test code
});
```

---

## Security Best Practices (PICKLES: Security)

### FLS Enforcement

```apex
// Always use SECURITY_ENFORCED or stripInaccessible
@AuraEnabled(cacheable=true)
public static List<Account> getAccounts() {
    return [SELECT Id, Name FROM Account WITH SECURITY_ENFORCED];
}

// For DML operations
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.CREATABLE,
    records
);
insert decision.getRecords();
```

### Input Sanitization

```apex
// Apex should escape user input
String searchKey = '%' + String.escapeSingleQuotes(searchTerm) + '%';
```

### XSS Prevention

LWC automatically escapes content in templates. Never bypass this.

```html
<!-- Safe: LWC auto-escapes -->
<p>{userInput}</p>
```

---

## Accessibility (a11y)

### Required Practices

| Element | Requirement |
|---------|-------------|
| Buttons | `label` or `aria-label` |
| Icons | `alternative-text` |
| Form inputs | Associated `<label>` |
| Dynamic content | `aria-live` region |
| Loading states | `aria-busy="true"` |

### Keyboard Navigation

```javascript
handleKeyDown(event) {
    switch (event.key) {
        case 'Enter':
        case ' ':
            this.handleSelect(event);
            break;
        case 'Escape':
            this.handleClose();
            break;
        case 'ArrowDown':
            this.focusNext();
            event.preventDefault();
            break;
    }
}
```

### Focus Trap Pattern (for Modals)

Based on [James Simone's modal pattern](https://www.jamessimone.net/blog/joys-of-apex/lwc-composable-modal/):

```javascript
_focusableElements = [];

_onOpen() {
    // Collect focusable elements
    this._focusableElements = [
        ...this.querySelectorAll('.focusable'),
        ...this.template.querySelectorAll('lightning-button, button, [tabindex="0"]')
    ].filter(el => !el.disabled);

    // Focus first element
    this._focusableElements[0]?.focus();

    // Add ESC handler
    window.addEventListener('keyup', this._handleKeyUp);
}

_handleKeyUp = (event) => {
    if (event.code === 'Escape') {
        this.close();
    }
}

disconnectedCallback() {
    window.removeEventListener('keyup', this._handleKeyUp);
}
```

---

## SLDS 2 & Dark Mode

### Dark Mode Checklist

- [ ] No hardcoded hex colors (`#FFFFFF`, `#333333`)
- [ ] No hardcoded RGB/RGBA values
- [ ] All colors use CSS variables (`var(--slds-g-color-*)`)
- [ ] Fallback values provided for SLDS 1 compatibility
- [ ] Icons use SLDS utility icons (auto-adjust for dark mode)

### SLDS 1 → SLDS 2 Migration

```css
/* BEFORE (SLDS 1 - Deprecated) */
.my-card {
    background-color: #ffffff;
    color: #333333;
}

/* AFTER (SLDS 2 - Dark Mode Ready) */
.my-card {
    background-color: var(--slds-g-color-surface-container-1, #ffffff);
    color: var(--slds-g-color-on-surface, #181818);
}
```

### Key Global Styling Hooks

| Category | SLDS 2 Variable |
|----------|-----------------|
| Surface | `--slds-g-color-surface-1` to `-4` |
| Text | `--slds-g-color-on-surface` |
| Border | `--slds-g-color-border-1`, `-2` |
| Spacing | `--slds-g-spacing-0` to `-12` |

**Important**: `--slds-c-*` (component-level hooks) are NOT supported in SLDS 2 yet.

---

## Testing Checklist

### Unit Test Coverage

- [ ] Component renders without errors
- [ ] Data displays correctly when loaded
- [ ] Error state displays when fetch fails
- [ ] Empty state displays when no data
- [ ] Events dispatch with correct payload
- [ ] User interactions work correctly
- [ ] Loading states are shown/hidden appropriately

### Manual Testing

- [ ] Works in Lightning Experience
- [ ] Works in Salesforce Mobile
- [ ] Works in Experience Cloud (if targeted)
- [ ] Works in Dark Mode (SLDS 2)
- [ ] Keyboard navigation works
- [ ] Screen reader announces properly
- [ ] No console errors
- [ ] Performance acceptable with real data

---

## Common Mistakes

### 1. Modifying @api Properties

```javascript
// ❌ BAD
@api items;
handleClick() {
    this.items.push(newItem);  // Mutation!
}

// ✅ GOOD
handleClick() {
    this.items = [...this.items, newItem];
}
```

### 2. Forgetting to Clean Up

```javascript
// ❌ BAD: Memory leak
connectedCallback() {
    this.subscription = subscribe(...);
}

// ✅ GOOD
disconnectedCallback() {
    unsubscribe(this.subscription);
}
```

### 3. Wire with Non-Reactive Parameters

```javascript
// ❌ BAD
let recordId = '001xxx';
@wire(getRecord, { recordId: recordId })

// ✅ GOOD
@api recordId;
@wire(getRecord, { recordId: '$recordId' })
```

---

## Resources

- [PICKLES Framework (Salesforce Ben)](https://www.salesforceben.com/the-ideal-framework-for-architecting-salesforce-lightning-web-components/)
- [LWC Recipes (GitHub)](https://github.com/trailheadapps/lwc-recipes)
- [SLDS 2 Transition Guide](https://www.lightningdesignsystem.com/2e1ef8501/p/8184ad-transition-to-slds-2)
- [James Simone - Advanced Jest Testing](https://www.jamessimone.net/blog/joys-of-apex/advanced-lwc-jest-testing/)
- [James Simone - Composable Modal](https://www.jamessimone.net/blog/joys-of-apex/lwc-composable-modal/)
- [SLDS Styling Hooks](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-custom-properties.html)
