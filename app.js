const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");
const uuid = require("uuid");

const app = express();
app.use(cors());

// Set up file storage with multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, "uploads/");
    },
    filename: (req, file, cb) => {
        const filename = `${uuid.v4()}-${file.originalname}`;
        cb(null, filename);
    }
});

const upload = multer({ storage: storage });

// Serve the "uploads" directory as static files
app.use(express.static('uploads'));
app.use(express.static('public'));

// Define the route for uploading the CSV
app.post("/upload-csv", upload.single("csv"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const inputCsvPath = path.join(__dirname, "uploads", req.file.filename);
    const outputCsvPath = path.join(__dirname, "uploads", `processed-${req.file.filename}`);

    // Call the Python script to process the CSV
    const pythonProcess = spawn("python", ["algorithm.py", inputCsvPath, outputCsvPath]);

    let isResponseSent = false; // Track if a response has already been sent

    // Handle Python script stdout (processed CSV file path)
    pythonProcess.stdout.on("data", (data) => {
        if (isResponseSent) return; // Avoid sending duplicate responses

        try {
            const result = JSON.parse(data.toString());
            const outputFile = result.output_file;

            // Send the output file URL as a response
            res.json({
                message: "CSV processed successfully",
                output_file: `/uploads/${path.basename(outputFile)}`
            });
            isResponseSent = true;
        } catch (error) {
            if (!isResponseSent) {
                console.error("Error parsing Python script output:", error.message);
                res.status(500).json({ error: "Error processing CSV output" });
                isResponseSent = true;
            }
        }
    });

    // Handle Python script stderr (errors)
    pythonProcess.stderr.on("data", (data) => {
        if (!isResponseSent) {
            console.error("Error in Python script:", data.toString());
            res.status(500).json({ error: "Error processing CSV" });
            isResponseSent = true;
        }
    });

    // Handle Python process exit event
    pythonProcess.on("close", (code) => {
        if (!isResponseSent) {
            if (code === 0) {
                console.log("Python script executed successfully.");
            } else {
                console.error(`Python script exited with code ${code}`);
                res.status(500).json({ error: "Python script execution failed" });
            }
            isResponseSent = true;
        }
    });
});

// Serve the front-end HTML page
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start the Express app
const port = 5000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
