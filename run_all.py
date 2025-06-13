import json
import random
import os
import http.server
import socketserver
import webbrowser
import threading
import time
import subprocess
import sys
import csv
import math

# Create the example/basic directory if it doesn't exist
os.makedirs("example/basic", exist_ok=True)

# Global variables
visited_nodes = set()  # Track nodes visited during influence propagation

# Kill any process using port 8080 on Windows
def kill_process_on_port(port):
    try:
        # Find process using the port
        result = subprocess.run(['netstat', '-ano', '|', 'findstr', f':{port}'], 
                              shell=True, capture_output=True, text=True)
        
        for line in result.stdout.strip().split('\n'):
            if f':{port}' in line:
                parts = line.strip().split()
                if len(parts) > 4:
                    pid = parts[4]
                    print(f"Killing process with PID {pid} using port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                  shell=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")
        return False

# Try to kill process on port 8080
PORT = 8080
if not kill_process_on_port(PORT):
    # If we couldn't kill the process, try an alternative port
    PORT = 8081
    if not kill_process_on_port(PORT):
        # If that's also taken, try one more
        PORT = 8082

# Convert short company name to full name
def get_full_company_name(short_name):
    prefix = short_name.split('_')[0]
    number = short_name.split('_')[2]
    
    prefixes = {
        'TRA': 'Transportation Company',
        'ENE': 'Energy Corporation',
        'MAN': 'Manufacturing Industries',
        'INF': 'Information Technology Solutions',
        'FIN': 'Financial Services',
        'RET': 'Retail Enterprises',
        'HEA': 'Healthcare Provider',
        'CON': 'Construction Group',
        'AGR': 'Agricultural Products',
        'TEL': 'Telecommunications Network',
        'EDU': 'Educational Institution',
        'MED': 'Media Productions',
        'MIN': 'Mining Operations',
        'GOV': 'Government Agency',
        'WAS': 'Waste Management Services'
    }
    
    if prefix in prefixes:
        return f"{prefixes[prefix]} {number}"
    else:
        return short_name  # Return original if prefix not found

# Read companies from CSV
companies = {}
sectors = set()
try:
    # Try to read from companies_400.csv first
    with open('companies_400.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company_id = row['Company']
            sector = row['Sector']
            # For the new format, use the company_id as the full name since they are already descriptive
            full_name = company_id
            companies[company_id] = {'name': full_name, 'sector': sector, 'green_score': random.randint(20, 80)}
            sectors.add(sector)
    print(f"Successfully loaded {len(companies)} companies from companies_400.csv")
except Exception as e:
    print(f"Error reading companies_400.csv: {e}")
    print("Trying to read companies.csv instead...")
    
    try:
        with open('companies.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_id = row['Company']
                sector = row['Sector']
                full_name = get_full_company_name(company_id)
                companies[company_id] = {'name': full_name, 'sector': sector, 'green_score': random.randint(20, 80)}
                sectors.add(sector)
        print(f"Successfully loaded {len(companies)} companies from companies.csv")
    except Exception as e:
        print(f"Error reading companies.csv: {e}")
        print("Generating random company data instead...")
        
        # Generate some random companies if the file can't be read
        sectors = ["Transportation", "Energy", "Manufacturing", "Information Technology", 
                  "Finance", "Retail", "Healthcare", "Construction", "Agriculture", 
                  "Telecommunications", "Education", "Media", "Mining", "Government", 
                  "Waste Management"]
        
        for sector in sectors:
            for i in range(1, 21):
                company_id = f"{sector[:3].upper()}_Co_{i}"
                full_name = get_full_company_name(company_id)
                companies[company_id] = {'name': full_name, 'sector': sector, 'green_score': random.randint(20, 80)}

# Assign a color to each sector
sector_colors = {}
colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5"
]

for i, sector in enumerate(sectors):
    sector_colors[sector] = colors[i % len(colors)]

# Create nodes
nodes = []
company_id_to_index = {}
for i, (company_id, info) in enumerate(companies.items()):
    nodes.append({
        "id": company_id,
        "name": info['name'],
        "sector": info['sector'],
        "val": info['green_score'],
        "color": sector_colors[info['sector']]
    })
    company_id_to_index[company_id] = i

# Read edges from CSV
edges = []
graph_connections = {}  # Store connections for influence calculations

try:
    # Try to read from edges_400.csv first
    with open('edges_400.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company1 = row['Company1']
            company2 = row['Company2']
            weight = float(row['Weight'])
            
            if company1 in companies and company2 in companies:
                edges.append({
                    "source": company1,
                    "target": company2,
                    "value": weight
                })
                
                # Add to connections graph (for both directions to make it undirected)
                if company1 not in graph_connections:
                    graph_connections[company1] = {}
                if company2 not in graph_connections:
                    graph_connections[company2] = {}
                
                graph_connections[company1][company2] = weight
                graph_connections[company2][company1] = weight
    
    print(f"Successfully loaded {len(edges)} edges from edges_400.csv")
except Exception as e:
    print(f"Error reading edges_400.csv: {e}")
    print("Trying to read edges_weights.csv instead...")
    
    try:
        with open('edges_weights.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company1 = row['Company1']
                company2 = row['Company2']
                weight = float(row['Weight'])
                
                if company1 in companies and company2 in companies:
                    edges.append({
                        "source": company1,
                        "target": company2,
                        "value": weight
                    })
                    
                    # Add to connections graph (for both directions to make it undirected)
                    if company1 not in graph_connections:
                        graph_connections[company1] = {}
                    if company2 not in graph_connections:
                        graph_connections[company2] = {}
                    
                    graph_connections[company1][company2] = weight
                    graph_connections[company2][company1] = weight
        
        print(f"Successfully loaded {len(edges)} edges from edges_weights.csv")
    except Exception as e:
        print(f"Error reading edges_weights.csv: {e}")
        print("Generating random edges instead...")
        
        # Generate random edges if file can't be read
        company_ids = list(companies.keys())
        num_companies = len(company_ids)
        
        # Create a more spread out graph with fewer but meaningful connections
        for i, company_id in enumerate(company_ids):
            # Each company connects to 3-6 other companies
            num_connections = random.randint(3, 6)
            connected = set()
            
            for _ in range(num_connections):
                # Select a target that isn't already connected
                while True:
                    target_idx = random.randint(0, num_companies - 1)
                    target_id = company_ids[target_idx]
                    
                    # Skip self-connections and existing connections
                    if target_id != company_id and target_id not in connected:
                        break
                
                connected.add(target_id)
                weight = round(random.uniform(0.1, 3.0), 2)
                
                edges.append({
                    "source": company_id,
                    "target": target_id,
                    "value": weight
                })
                
                # Add to connections graph
                if company_id not in graph_connections:
                    graph_connections[company_id] = {}
                if target_id not in graph_connections:
                    graph_connections[target_id] = {}
                    
                graph_connections[company_id][target_id] = weight
                graph_connections[target_id][company_id] = weight

# Calculate influences for a node
def calculate_influences(node_id):
    if node_id not in graph_connections:
        return []
    
    influencers = []
    for connected_id, weight in graph_connections[node_id].items():
        # Calculate influence based on weight and the connected node's green score
        connected_green_score = companies[connected_id]['green_score']
        influence = round(weight * connected_green_score / 100, 2)  # Normalize influence
        
        influencers.append({
            "id": connected_id,
            "name": companies[connected_id]['name'],
            "influence": influence  # Kept as "influence" for backend compatibility
        })
    
    # Sort by influence (highest first)
    influencers.sort(key=lambda x: x["influence"], reverse=True)
    
    return influencers

# Propagate influence when a green score changes
def propagate_influence(node_id, new_green_score):
    # Update the node's green score
    if node_id in companies:
        old_score = companies[node_id]['green_score']
        companies[node_id]['green_score'] = new_green_score
        
        # Track all nodes that are affected
        global visited_nodes
        visited_nodes = set([node_id])  # Make this accessible to the API handler
        
        # Update the corresponding node in the nodes list
        for node in nodes:
            if node["id"] == node_id:
                node["val"] = new_green_score
                break
        
        # Propagate influence to connected nodes
        if node_id in graph_connections:
            nodes_to_update = [(connected_id, weight) for connected_id, weight in graph_connections[node_id].items()]
            
            # Process nodes in layers (breadth-first)
            level = 0
            max_levels = 3  # Limit the propagation to 3 levels
            
            while nodes_to_update and level < max_levels:
                next_level = []
                
                for update_id, weight in nodes_to_update:
                    if update_id in visited_nodes:
                        continue
                        
                    visited_nodes.add(update_id)
                    
                    # Calculate influence factor (decreasing with each level)
                    influence_factor = weight * (0.7 ** level)
                    
                    # The delta is based on the change in the original node's score
                    score_delta = new_green_score - old_score
                    
                    # Update the connected node's green score proportionally
                    if update_id in companies:
                        update_amount = score_delta * influence_factor * 0.25  # Dampen the effect
                        companies[update_id]['green_score'] = max(0, min(100, companies[update_id]['green_score'] + update_amount))
                        
                        # Update the node in the nodes list
                        for node in nodes:
                            if node["id"] == update_id:
                                node["val"] = companies[update_id]['green_score']
                                break
                        
                        # Add connected nodes to the next level
                        if update_id in graph_connections:
                            for next_id, next_weight in graph_connections[update_id].items():
                                if next_id not in visited_nodes:
                                    next_level.append((next_id, next_weight))
                
                nodes_to_update = next_level
                level += 1
        
        # Save updated graph data
        with open("example/basic/graph.json", "w") as f:
            json.dump({"nodes": nodes, "links": edges}, f, indent=2)
        
        return True
    
    return False

# Save initial graph data to file
with open("example/basic/graph.json", "w") as f:
    json.dump({"nodes": nodes, "links": edges}, f, indent=2)

print("Graph data generated successfully!")

# Create a simple server handler
class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API endpoints
        if self.path == '/api/graph':
            # Serve the graph data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read the graph data from the pre-generated file
            try:
                with open('example/basic/graph.json', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(json.dumps({"error": "Graph data not found"}).encode())
                
        elif self.path.startswith('/api/influences/'):
            # Extract node ID and decode URL encoding
            node_id = self.path.split('/')[-1]
            # Handle URL encoding for node IDs with spaces
            node_id = node_id.replace('%20', ' ')
            
            # Get the node name
            node_name = "Unknown"
            for node in nodes:
                if node["id"] == node_id:
                    node_name = node["name"]
                    break
            
            # Calculate influencers for the node
            influencers = calculate_influences(node_id)
            
            response = {
                "nodeId": node_id,
                "nodeName": node_name,
                "influencers": influencers
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path.startswith('/api/update_green_score/'):
            # Extract info from path: /api/update_green_score/{nodeId}/{score}
            parts = self.path.split('/')
            node_id = parts[-2]
            # Handle URL encoding for node IDs with spaces
            node_id = node_id.replace('%20', ' ')
            
            try:
                new_score = float(parts[-1])
                
                # Validate score
                if new_score < 0 or new_score > 100:
                    raise ValueError("Score must be between 0 and 100")
                
                # Update and propagate
                success = propagate_influence(node_id, new_score)
                
                # Get updated nodes and their influencers
                updated_nodes = []
                updated_influencers = {}
                for node in nodes:
                    if node["id"] in visited_nodes:  # This is from propagate_influence
                        updated_nodes.append(node)
                        # Get influencers for this node if it was updated
                        if node["id"] == node_id:
                            updated_influencers = {
                                "nodeId": node_id,
                                "nodeName": node["name"],
                                "influencers": calculate_influences(node_id)
                            }
                
                response = {
                    "success": success,
                    "message": "Green score updated successfully" if success else "Failed to update green score",
                    "updatedNodes": updated_nodes,
                    "updatedInfluencers": updated_influencers
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except (ValueError, IndexError) as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            
        else:
            # Serve static files
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Function to open browser after server starts
def open_browser():
    time.sleep(1)  # Give the server a second to start
    url = f"http://localhost:{PORT}/example/basic/"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

# Start the browser in a separate thread
browser_thread = threading.Thread(target=open_browser)
browser_thread.daemon = True
browser_thread.start()

# Start the server
print(f"Starting server on port {PORT}")
try:
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()
except OSError as e:
    if "Address already in use" in str(e):
        print(f"ERROR: Port {PORT} is still in use!")
        print("Please manually kill any process using this port.")
        print("You can run these commands in Command Prompt:")
        print(f"1. netstat -ano | findstr :{PORT}")
        print("2. taskkill /F /PID <PID_NUMBER>")
        sys.exit(1)
    else:
        print(f"ERROR: {e}")
        sys.exit(1)
