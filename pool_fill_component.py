# pool_fill_component.py

import streamlit.components.v1 as components

# Define the React component as a string of JavaScript code
pool_fill_component = """
const {useState, useEffect} = React;

const PoolFill = ({initialFillPercentage = 50}) => {
  const [fillPercentage, setFillPercentage] = useState(initialFillPercentage);

  useEffect(() => {
    setFillPercentage(initialFillPercentage);
  }, [initialFillPercentage]);

  return (
    React.createElement('div', {className: 'flex flex-col items-center w-full max-w-md mx-auto'},
      React.createElement('div', {className: 'w-full h-64 bg-blue-100 border-4 border-blue-500 rounded-lg overflow-hidden relative mb-4'},
        React.createElement('div', {
          className: 'absolute bottom-0 left-0 right-0 bg-blue-500 transition-all duration-300 ease-in-out',
          style: { height: `${fillPercentage}%` }
        })
      ),
      React.createElement('input', {
        type: 'range',
        min: 0,
        max: 100,
        value: fillPercentage,
        onChange: (e) => setFillPercentage(Number(e.target.value)),
        className: 'w-full'
      }),
      React.createElement('p', {className: 'mt-2 text-lg font-semibold'},
        `Pool is ${fillPercentage.toFixed(2)}% full`
      )
    )
  );
};

// Render the component
ReactDOM.render(
  React.createElement(PoolFill, {initialFillPercentage: streamlitInitialFillPercentage}),
  document.getElementById('root')
)
"""

# Function to create the custom component
def pool_fill(initial_fill_percentage):
    component = components.declare_component(
        "pool_fill",
        path=".",  # This is required for Streamlit Cloud
    )
    return component(initialFillPercentage=initial_fill_percentage)

# Helper function to use in the main app
def st_pool_fill(initial_fill_percentage):
    components.html(
        f"""
        <div id="root"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0.2/umd/react.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/17.0.2/umd/react-dom.production.min.js"></script>
        <script>
            const streamlitInitialFillPercentage = {initial_fill_percentage};
            {pool_fill_component}
        </script>
        """,
        height=400,
    )
