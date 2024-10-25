const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware to parse JSON requests
app.use(express.json());

// Endpoint to save GeoJSON file
app.post('/save_geojson', (req, res) => {
    const geojsonData = req.body;
    
    // Path to save the file
    const filePath = path.join(__dirname, 'saved_geojson', 'polygon_data.geojson');

    // Write the GeoJSON data to a file
    fs.writeFile(filePath, JSON.stringify(geojsonData, null, 2), (err) => {
        if (err) {
            console.error('Error writing file:', err);
            res.status(500).json({ message: 'Failed to save file' });
        } else {
            console.log('File saved:', filePath);
            res.json({ message: 'File saved successfully', filePath });
        }
    });
});

// Start the server
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
