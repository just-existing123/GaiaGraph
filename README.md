# Green Score Graph Visualization Platform

## 📋 Table of Contents
1. [🚀 Quick Start](#-quick-start)
2. [🌟 Project Overview](#-project-overview)
3. [📁 Repository Structure](#-repository-structure)
4. [🏗️ Technology Stack](#️-technology-stack)
5. [🧠 Backend: Advanced Analytics Engine](#-backend-advanced-analytics-engine)
6. [🎨 Frontend: JavaScript Libraries](#-frontend-javascript-libraries)
7. [⚙️ Installation & Setup](#️-installation--setup)
8. [📚 Usage Guide](#-usage-guide)
9. [🔌 API Documentation](#-api-documentation)
10. [🔬 Algorithm Analysis](#-algorithm-analysis)
11. [⚡ Performance & Optimization](#-performance--optimization)
12. [⚙️ Configuration](#️-configuration)
13. [🤝 Contributing](#-contributing)

---

## 🌟 Project Overview

This is a comprehensive platform for analyzing, simulating, and visualizing influence networks among companies based on their environmental ("green") scores. The project combines a high-performance **C++ backend** for advanced graph analytics with a **React-based frontend** for interactive visualization.

### Key Features
- **Environmental Impact Analysis**: Multi-factor green score calculation
- **Network Modeling**: Directed, weighted dependency graphs
- **Influence Simulation**: Real-time propagation analysis
- **Maximum Flow Analysis**: Critical pathway identification
- **Multi-modal Visualization**: 2D, 3D, VR, and AR rendering
- **Real-time Updates**: Live graph modifications and influence propagation

---

## 📁 Repository Structure
```
react-force-graph-master/
├── Backend/                    # C++ Analytics Engine
│   ├── Company.h/.cpp         # Company data structures
│   ├── Graph.h/.cpp           # Graph representation
│   ├── GreenScoreCalculator.h/.cpp  # Environmental scoring
│   ├── InfluenceCalculator.h/.cpp   # Influence propagation
│   ├── MaxFlowCalculator.h/.cpp     # Maximum flow analysis
│   ├── ScalingFactor.h/.cpp   # Sector scaling factors
│   └── main.cpp               # Main application
├── src/                       # React Components
│   ├── packages/              # Individual packages
│   │   ├── react-force-graph-2d/   # 2D Canvas implementation
│   │   ├── react-force-graph-3d/   # 3D WebGL implementation
│   │   ├── react-force-graph-vr/   # VR A-Frame implementation
│   │   └── react-force-graph-ar/   # AR implementation
│   ├── forcegraph-proptypes.js     # PropTypes definitions
│   └── index.js               # Main exports
├── example/                   # Demo Applications
│   ├── basic/                 # Green score visualization
│   ├── datasets/              # Sample data files
│   └── [other examples]/     # Various visualization demos
├── run_all.py                 # Python server & data generator
├── package.json               # Main package configuration
└── rollup.config.js           # Build configuration
```

---

## 🏗️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | C++17 + STL | High-performance graph algorithms |
| **Frontend** | React 18 | Component-based UI framework |
| **2D Rendering** | Canvas API + D3-force | High-performance 2D visualization |
| **3D Rendering** | Three.js + WebGL | Hardware-accelerated 3D graphics |
| **VR Support** | A-Frame + WebXR | Virtual reality experiences |
| **AR Support** | AR.js | Augmented reality visualization |
| **Integration** | Python HTTP Server | REST API and data processing |
| **Data Format** | JSON/CSV | Standardized data exchange |

---

## 🧠 Backend: Advanced Analytics Engine

### Core Responsibilities
- **Environmental Score Calculation**: Multi-factor environmental impact assessment
- **Graph Network Modeling**: Directed, weighted dependency relationships
- **Influence Propagation Simulation**: Modified BFS with decay factors
- **Maximum Flow Analysis**: Critical pathway identification using Edmonds-Karp
- **Data Processing Pipeline**: CSV/JSON ingestion and transformation
- **Performance Optimization**: Efficient algorithms for large-scale networks

### Key Backend Components

#### 1. Company Data Structure (`Company.h/.cpp`)
```cpp
class Company {
    Graph::ID id;
    std::string name;
    std::string sector;
    double baseGreenScore;
    double adjustedGreenScore;
};
```
- Represents individual companies with environmental metrics
- Stores sector-specific information for scaling calculations
- Manages both base and adjusted green scores

#### 2. Graph Representation (`Graph.h/.cpp`)
- **Adjacency List**: `std::unordered_map<ID, std::vector<std::pair<ID, double>>>`
- **Edge Management**: Support for edge ignoring and cycle prevention
- **Weighted Relationships**: Influence strength modeling
- **Traversal Utilities**: BFS, DFS, and custom algorithms

#### 3. Green Score Calculator (`GreenScoreCalculator.h/.cpp`)
- **Multi-factor Assessment**: Factory emissions, employee footprint, vehicle emissions
- **Sector Normalization**: Industry-specific scaling factors
- **Score Range**: Normalized to -100 to +100 scale
- **Real-time Updates**: Dynamic recalculation capabilities

#### 4. Influence Propagation Algorithm (`InfluenceCalculator.h/.cpp`)
- **Modified BFS Traversal**: Queue-based breadth-first processing
- **Decay Modeling**: Exponential attenuation over network distance
- **Path Optimization**: Maximum influence path selection
- **Cycle Prevention**: Visited node tracking and edge ignoring

#### 5. Maximum Flow Calculator (`MaxFlowCalculator.h/.cpp`)
- **Edmonds-Karp Implementation**: BFS-based augmenting path detection
- **Residual Graph Management**: Dynamic capacity updates
- **Path Decomposition**: Individual flow path identification
- **JSON Output**: Structured results for visualization

#### 6. Scaling Factor Manager (`ScalingFactor.h/.cpp`)
- **JSON Configuration**: Loads sector-specific multipliers
- **Dynamic Updates**: Runtime modification of scaling factors
- **Validation**: Ensures data integrity and proper formatting

### Advanced Algorithms Deep Dive

#### Modified BFS for Influence Propagation
The influence propagation algorithm uses a sophisticated approach that can be conceptually understood as an "inverted Dijkstra" with maximum heap optimization:

```cpp
std::unordered_map<Graph::ID, double> InfluenceCalculator::computeInfluence(
    const Graph& graph, Graph::ID sourceID) {
    
    std::unordered_map<Graph::ID, double> influences;
    std::queue<std::pair<Graph::ID, double>> q;
    std::unordered_set<Graph::ID> visited;
    
    // Initialize with source node
    q.push({sourceID, 1.0});
    influences[sourceID] = 1.0;
    visited.insert(sourceID);
    
    while (!q.empty()) {
        auto [currentID, currentInfluence] = q.front();
        q.pop();
        
        // Propagate to neighbors with decay
        for (const auto& [neighborID, weight] : graph.getAdjacent(currentID)) {
            if (graph.isEdgeIgnored(currentID, neighborID)) continue;
            
            double propagatedInfluence = currentInfluence * weight * DECAY_FACTOR;
            
            // Keep maximum influence path
            if (influences.find(neighborID) == influences.end() || 
                propagatedInfluence > influences[neighborID]) {
                influences[neighborID] = propagatedInfluence;
                
                if (visited.find(neighborID) == visited.end()) {
                    visited.insert(neighborID);
                    q.push({neighborID, propagatedInfluence});
                }
            }
        }
    }
    
    return influences;
}
```

#### Edmonds-Karp Maximum Flow Algorithm
```cpp
double MaxFlowCalculator::fordFulkerson(/* parameters */) {
    double maxFlow = 0.0;
    std::unordered_map<Graph::ID, Graph::ID> parent;
    
    // Find augmenting paths using BFS
    while (bfs(capacities, adjacencyList, flow, sourceID, sinkID, parent)) {
        // Find bottleneck capacity
        double pathFlow = std::numeric_limits<double>::max();
        for (Graph::ID v = sinkID; v != sourceID; v = parent[v]) {
            Graph::ID u = parent[v];
            pathFlow = std::min(pathFlow, capacities[u][v] - flow[u][v]);
        }
        
        // Update residual capacities
        for (Graph::ID v = sinkID; v != sourceID; v = parent[v]) {
            Graph::ID u = parent[v];
            flow[u][v] += pathFlow;
            flow[v][u] -= pathFlow;
        }
        
        maxFlow += pathFlow;
    }
    
    return maxFlow;
}
```

### Data Processing Pipeline
- **CSV Parsing**: Robust handling of company and edge data
- **JSON Configuration**: Sector scaling factors and output formatting
- **Error Handling**: Comprehensive validation and error reporting
- **Performance Metrics**: Algorithm timing and memory usage tracking

---

## 🎨 Frontend: JavaScript Libraries

The frontend provides interactive graph visualization through React components that integrate multiple JavaScript libraries:

### Core Libraries
- **React 18** - Component framework and state management
- **react-kapsule** - Bridge between D3 components and React lifecycle
- **prop-types** - Runtime type checking for React props

### Visualization Libraries
- **force-graph** - 2D Canvas-based rendering with D3-force physics
- **3d-force-graph** - Three.js WebGL rendering with 3D physics
- **3d-force-graph-vr** - A-Frame integration for VR experiences  
- **3d-force-graph-ar** - AR.js integration for augmented reality
- **d3-force-3d** - Extended D3 force simulation for 3D space
- **three.js** - 3D graphics library for WebGL rendering
- **aframe** - Web framework for building VR experiences
- **ar.js** - Augmented reality library for marker tracking

### Integration Points
- **REST API Communication** - Interfaces with Python server via HTTP
- **Real-time Data Updates** - Polling mechanism for live graph changes
- **Multi-format Exports** - UMD/ESM module support via Rollup bundler
- **JSON Data Protocol** - Standardized exchange format with backend

---

## ⚙️ Installation & Setup

### Prerequisites
- **Node.js** (v14 or higher)
- **Python** (v3.7 or higher)
- **C++ Compiler** (GCC, Clang, or MSVC with C++17 support)

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/react-force-graph-master.git
   cd react-force-graph-master
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the application:**
   ```bash
   # Windows
   start.bat
   
   # Cross-platform
   python run_all.py
   ```

4. **Access the application:**
   Navigate to `http://localhost:8080/example/basic/`

### Manual Backend Compilation
```bash
cd Backend
g++ -std=c++17 -O3 -o green_score_analysis \
    main.cpp Company.cpp Graph.cpp \
    GreenScoreCalculator.cpp InfluenceCalculator.cpp \
    MaxFlowCalculator.cpp ScalingFactor.cpp
./green_score_analysis
```

---

## 🚀 Quick Start

### One-Command Setup
```bash
# Windows - Double-click or run in PowerShell
start.bat

# Cross-platform alternative
python run_all.py
```
This will automatically:
- Generate sample graph data
- Start the Python web server 
- Open your browser at [http://localhost:8080/example/basic/](http://localhost:8080/example/basic/)

### What You'll See
- Interactive 2D/3D graph visualization
- Companies represented as colored nodes (by sector)
- Real-time influence propagation when green scores change
- Click nodes to view details and adjust environmental scores

---

## 📚 Usage Guide

### Basic Example
```jsx
import ForceGraph3D from 'react-force-graph-3d';

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    fetch('/api/graph')
      .then(res => res.json())
      .then(setGraphData);
  }, []);

  return (
    <ForceGraph3D
      graphData={graphData}
      nodeAutoColorBy="sector"
      nodeLabel="name"
      onNodeClick={(node) => console.log('Node clicked:', node)}
    />
  );
}
```

### Data Format
```json
{
  "nodes": [
    {
      "id": "TRA_Co_1",
      "name": "Transportation Company 1",
      "sector": "Transportation",
      "val": 75.2,
      "color": "#1f77b4"
    }
  ],
  "links": [
    {
      "source": "TRA_Co_1",
      "target": "ENE_Co_2",
      "value": 2.5
    }
  ]
}
```

---

## 🔌 API Documentation

### Endpoints

#### GET `/api/graph`
Returns the complete graph data structure.

#### GET `/api/influences/{nodeId}`
Returns influence relationships for a specific node.

**Response:**
```json
{
  "nodeId": "TRA_Co_1",
  "nodeName": "Transportation Company 1",
  "influencers": [
    {
      "id": "ENE_Co_2",
      "name": "Energy Corporation 2",
      "influence": 1.85
    }
  ]
}
```

#### GET `/api/update_green_score/{nodeId}/{score}`
Updates a company's green score and propagates influence.

**Parameters:**
- `nodeId`: Company identifier
- `score`: New green score (0-100)

---

## 🔬 Algorithm Analysis

### Influence Propagation vs. Dijkstra's Algorithm

The modified BFS traversal for influence propagation can be understood as an "inverted Dijkstra" algorithm:

**Similarities:**
- Priority-based traversal
- Visited node tracking
- Value updates during traversal

**Key Differences:**
- **Optimization Direction**: Maximizes influence vs. minimizes distance
- **Value Propagation**: Multiplicative decay vs. additive weights
- **Path Selection**: Strongest influence vs. shortest path
- **Termination**: Influence threshold vs. target reached

```cpp
// Traditional Dijkstra (minimum distance)
while (!pq.empty()) {
    auto [distance, node] = pq.top();
    pq.pop();
    
    for (auto [neighbor, weight] : adj[node]) {
        int newDist = distance + weight;  // Additive
        if (newDist < dist[neighbor]) {   // Minimize
            dist[neighbor] = newDist;
            pq.push({newDist, neighbor});
        }
    }
}

// Influence Propagation (maximum influence)
while (!q.empty()) {
    auto [node, influence] = q.front();
    q.pop();
    
    for (auto [neighbor, weight] : adj[node]) {
        double newInfluence = influence * weight * decay;  // Multiplicative
        if (newInfluence > influences[neighbor]) {         // Maximize
            influences[neighbor] = newInfluence;
            q.push({neighbor, newInfluence});
        }
    }
}
```

---

## ⚡ Performance & Optimization

### Backend Optimizations
- **STL Containers**: Efficient `unordered_map` and `vector` usage
- **Memory Management**: Object pooling and resource cleanup
- **Algorithm Complexity**: O(V + E) for BFS, O(V²E) for max flow

### Frontend Optimizations
- **Level-of-Detail**: Automatic quality adjustment for large graphs
- **WebGL Rendering**: Hardware-accelerated 3D graphics
- **Physics Simulation**: Optimized force calculations

---

## ⚙️ Configuration

### Data Files
- `companies.csv`: Company data with sectors
- `edges_weights.csv`: Dependency relationships
- `scaling_factors.json`: Sector-specific multipliers

### Environment Variables
```javascript
const CONFIG = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8080',
  GRAPH_PHYSICS: {
    alphaDecay: 0.0228,
    velocityDecay: 0.4
  }
};
```

---
