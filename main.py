from graph import build_graph # Import the graph from graph

graph = build_graph()

def main():
    print("Welcome to the Order Support Agent!")
    print("enter exit to quit the program.\n")

    
    while True:
        query = input("Please enter your request (e.g., 'Cancel order ORD101', 'Track order ORD102', 'Check order ORD103'): ")

        if query.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break   

        state = {
            "query": query,
            "order_id": "",
            "intent": "",
            "response": "",
        }

        state = graph.invoke(state)

        print(state["response"])

if __name__ == "__main__":
    main()

    
