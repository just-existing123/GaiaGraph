# Green Score Graph Visualization

This project visualizes a network of companies and their green scores, showing the influence relationships between them.

## Features
- Interactive 3D graph visualization with dark background
- Node details panel showing green score and influencers
- Color-coded nodes based on sector
- Adjustable green scores with live influence propagation
- High-contrast edge visualization for clear network structure
- Animated directional particles showing influence flow
- Optimized graph layout for better node spacing
- Sector legend for easy reference
- Dark-themed UI for better visualization
- No automatic camera rotation for easier navigation

## Visual Enhancements
- Dark background with high-contrast UI elements
- Thicker, more visible white edges for better network visibility
- Brighter directional particles showing connection strength
- Optimized graph layout parameters for better spacing
- Green-themed UI elements matching the visualization context
- Enhanced controls for better user experience

## Real-time Updates
- When updating a node's green score, the changes are applied without refreshing the entire graph
- The graph maintains its layout and camera position during updates
- Edges and connections remain stable while nodes update
- The process is much faster and provides a seamless user experience

## How to Run

### Option 1: Quick Start (Recommended)
1. Double-click on `start.bat` in the project root
2. This will:
   - Kill any process using port 8080
   - Generate sample graph data
   - Start a Python web server
   - Open a browser window at http://localhost:8080/example/basic/

### Option 2: Manual Start
1. Open a command prompt
2. Navigate to the project directory
3. Run the Python script:
   ```
   python run_all.py
   ```
4. Open your browser to http://localhost:8080/example/basic/

## How to Use
- Click on any node to see its details in the info panel
- The info panel shows:
  - The node's full name
  - The node's sector
  - The node's current green score
  - A slider to edit the green score
  - A list of nodes that influence it
- Nodes are color-coded based on their sector (all companies in the same sector have the same color)
- Node size indicates green score (larger = higher green score)
- Edge width indicates the strength of relationship
- Use the "Freeze Graph" button in the top-right corner to stabilize the graph and prevent nodes from moving when updating green scores
- Click "Unfreeze Graph" to allow nodes to move again
- Adjusting a node's green score will automatically propagate influence to connected nodes
- The sector legend in the bottom-left shows the color coding for each sector

## Live Influence Propagation
When you change a node's green score:
1. Use the slider to set a new value
2. Click "Update Score"
3. The system will:
   - Update the selected node's green score
   - Propagate influence to connected nodes (up to 3 levels deep)
   - Update the graph visualization in real-time without resetting the layout
   - Update the influencers list immediately

## Technical Details
- Frontend: React with Force Graph 3D
- Backend: Python serving a RESTful API
- Data: Real company data from CSV files (`companies_400.csv` and `edges_400.csv`)
- Dataset: 400 companies across multiple sectors with real connection data
- Influence Calculation: Network propagation algorithm based on edge weights
- Color Coding: Consistent colors for companies in the same sector

## Troubleshooting
If the server fails to start with an "Address already in use" error:
1. Find the process using port 8080:
   ```
   netstat -ano | findstr :8080
   ```
2. Kill the process:
   ```
   taskkill /F /PID <PID_NUMBER>
   ```
   Replace `<PID_NUMBER>` with the PID shown in the previous step
3. Try running the server again
