import { app } from "../../scripts/app.js";

// Register the node styling when the extension is loaded
app.registerExtension({
    name: "draco.detail",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "AmateurFilter") {
            // Store the original onNodeCreated if it exists
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Override the onNodeCreated method to add custom styling
            nodeType.prototype.onNodeCreated = function() {
                // Call the original onNodeCreated if it exists
                if (onNodeCreated) {
                    onNodeCreated.apply(this, arguments);
                }
                
                // Set black and white color scheme
                this.color = "#222222";  // Node body color
                this.bgcolor = "#1a1a1a";  // Node background color
                
                // Set title bar color
                this.title_bgcolor = "#ffffff";  // White title background
                this.title_color = "#000000";  // Black title text
                
                // Ensure proper contrast
                this.shape = "box";
                
                // Add a custom property to identify this as a draco detail node
                this.properties = this.properties || {};
                this.properties.node_style = "draco_detail";
            };
        }
    }
});
