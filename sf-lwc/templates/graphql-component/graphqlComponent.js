/**
 * GraphQL Component Template
 *
 * Demonstrates the GraphQL wire adapter pattern for LWC with:
 * - GraphQL query definition using gql tagged template
 * - Cursor-based pagination
 * - Reactive variables
 * - Error handling
 * - Data transformation
 *
 * @see https://developer.salesforce.com/docs/platform/lwc/guide/data-graphql.html
 */
import { LightningElement, wire, track } from 'lwc';
import { gql, graphql, refreshGraphQL } from 'lightning/uiGraphQLApi';

// Define your GraphQL query using the gql tagged template literal
const CONTACTS_QUERY = gql`
    query ContactsWithAccount($first: Int!, $after: String, $orderBy: ContactOrderByInput) {
        uiapi {
            query {
                Contact(first: $first, after: $after, orderBy: $orderBy) {
                    edges {
                        node {
                            Id
                            Name { value }
                            Email { value }
                            Phone { value }
                            Title { value }
                            Account {
                                Id
                                Name { value }
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        endCursor
                        startCursor
                    }
                    totalCount
                }
            }
        }
    }
`;

export default class GraphqlComponent extends LightningElement {
    // Data state
    @track contacts = [];
    pageInfo;
    totalCount = 0;
    error;
    isLoading = true;

    // Pagination state
    _pageSize = 10;
    _cursor = null;

    // Store the wire result for refresh
    _wiredResult;

    /**
     * Wire the GraphQL query with reactive variables
     * Variables are recalculated whenever queryVariables getter returns new values
     */
    @wire(graphql, {
        query: CONTACTS_QUERY,
        variables: '$queryVariables'
    })
    wiredContacts(result) {
        this._wiredResult = result;
        const { data, error } = result;

        this.isLoading = false;

        if (data) {
            const queryResult = data.uiapi.query.Contact;

            // Transform GraphQL response to flat structure
            this.contacts = queryResult.edges.map(edge => ({
                id: edge.node.Id,
                name: edge.node.Name?.value,
                email: edge.node.Email?.value,
                phone: edge.node.Phone?.value,
                title: edge.node.Title?.value,
                accountId: edge.node.Account?.Id,
                accountName: edge.node.Account?.Name?.value,
                cursor: edge.cursor
            }));

            this.pageInfo = queryResult.pageInfo;
            this.totalCount = queryResult.totalCount;
            this.error = undefined;
        } else if (error) {
            this.error = this._reduceErrors(error);
            this.contacts = [];
        }
    }

    get queryVariables() {
        return {
            first: this._pageSize,
            after: this._cursor,
            orderBy: { Name: { order: 'ASC' } }
        };
    }

    get hasData() {
        return this.contacts.length > 0;
    }

    get hasNoData() {
        return !this.isLoading && !this.error && this.contacts.length === 0;
    }

    get hasNextPage() {
        return this.pageInfo?.hasNextPage;
    }

    get currentPageInfo() {
        return `Showing ${this.contacts.length} of ${this.totalCount} contacts`;
    }

    handleLoadMore() {
        if (this.hasNextPage) {
            this.isLoading = true;
            this._cursor = this.pageInfo.endCursor;
        }
    }

    handleRefresh() {
        this.isLoading = true;
        this._cursor = null;
        refreshGraphQL(this._wiredResult);
    }

    handleRowClick(event) {
        const contactId = event.currentTarget.dataset.id;
        this.dispatchEvent(new CustomEvent('contactselected', {
            detail: { contactId },
            bubbles: true,
            composed: true
        }));
    }

    _reduceErrors(errors) {
        if (!Array.isArray(errors)) {
            errors = [errors];
        }
        return errors
            .filter(error => !!error)
            .map(error => {
                if (typeof error === 'string') return error;
                if (error.body?.message) return error.body.message;
                if (error.message) return error.message;
                return 'Unknown error';
            })
            .join('; ');
    }
}
