const express = require('express');
const mongoose = require('mongoose');  
const User = require('./models/user');  
const bcrypt = require('bcrypt');  

const app = express();

const url = "mongodb+srv://ex-8:ebiznes@ex-8.vj9betn.mongodb.net/?retryWrites=true&w=majority&appName=ex-8"

async function connect(){
    try {
        await mongoose.connect(url);  
        console.log("Connected to MongoDB");  
    } catch(error){
        console.log(error);
    }
}
connect(); 
app.use(express.json()); 

app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    try {
        const existingUser = await User.findOne({ username: username });
        if (existingUser) {
            return res.status(409).send('User already exists.');
        }
        const user = new User({ username, password });
        await user.save();
        res.status(201).send('User created successfully.');
    } catch (error) {
        res.status(500).send('Server error: ' + error.message);
    }
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username: username });
    if (!user) {
        return res.status(401).send('Authentication failed: User not found.');
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
        return res.status(401).send('Authentication failed: Wrong password.');
    }
    res.send('Login successful!');
});

app.listen(8000, () => {
    console.log("Server started on port 8000");
});
