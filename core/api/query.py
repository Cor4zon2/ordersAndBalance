from ariadne import gql, QueryType, make_executable_schema
from ariadne.asgi import GraphQL

query = QueryType()

type_defs = gql("""
    type Query {
        balance: Balance!,
    }

    type Balance {
        balance: Int!
    }
""")

@query.field("balance")
def resolve_balance(*_):
    pass



schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)