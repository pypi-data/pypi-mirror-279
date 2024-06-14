"""
WARNING: always surround query data with single quotes. See orders_after_date_query
orders_after_date_query
  - variables: {"cursor": null, "numOrders" : 117, "query":"created_at:>'2023-02-18T06:00:00Z'"}

orders_after_order_number
  - variables: {"cursor": null, "numOrders" : 100, "query": "name:>#106900"}
  - WARNING: This query uses UTC time so beware of time changes!!
"""
order_followup_query = """
query {{orders(first: 250, after: null, reverse: true, query: {0}) {{
    pageInfo {{
      hasNextPage
      hasPreviousPage
    }}
    edges {{
      cursor
      node {{
        name
        createdAt
        customer {{
          firstName
          lastName
          email
          emailMarketingConsent {{
            marketingState                 
          }}
        }}
      }}
    }}
  }}
}}
"""

orders_after_date_query = """
query ($numOrders: Int!, $cursor: String, $query: String) {
  orders(first: $numOrders, after: $cursor, reverse: true, query:$query) {
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
    edges {
      cursor
      node {
        name
        createdAt
        customer {
          firstName
          lastName
          email
          emailMarketingConsent {
            marketingState                 
          }
        } 
      }
    }
  }
}"""

short_order_query = """query ($numOrders: Int!, $cursor: String) {
  orders(first: $numOrders, after: $cursor) {
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
    edges {
      cursor
      node {
        createdAt
        customer {
          firstName
          lastName
          emailMarketingConsent {
            marketingState                 
          }
          email
        } 
    }
  }
 }
}"""



order_query="""query ($numOrders: Int!, $cursor: String) {
  orders(first: $numOrders, after: $cursor) {
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
    edges {
      cursor
      node {
        id
        name
        discountCode
        createdAt
        customer {
          firstName
          lastName
          acceptsMarketing
          email
        }
        lineItems(first: 20) {
          edges {
            node {
              title
              sku
            }
          }
        }
      }
    }
  }
}
"""