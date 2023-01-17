require("dotenv").config();

const path = require("path");
const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const routes = require("./routes/routes");

const mongoString = process.env.DATABASE_URL;

mongoose.set("strictQuery", true);
mongoose.connect(mongoString);
const database = mongoose.connection;

database.on("error", (error) => {
  console.log(error);
});

database.once("connected", () => {
  console.log("Database Connected");
});

const app = express();

app.use(cors());
app.use(express.json());

// Add headers before the routes are defined
app.use(function (req, res, next) {
  // Website you wish to allow to connect
  res.setHeader("Access-Control-Allow-Origin", "https://localhost:443");

  // // Request methods you wish to allow
  // res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

  // // Request headers you wish to allow
  // res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

  // // Set to true if you need the website to include cookies in the requests sent
  // // to the API (e.g. in case you use sessions)
  // res.setHeader('Access-Control-Allow-Credentials', true);

  // Pass to next layer of middleware
  next();
});

app.use("/", routes);

console.log(
  path.resolve(__dirname, "..") +
    "\\video\\video-content\\thumbnail\\prelim-thumbnail"
);
app.use(
  "/images",
  express.static(
    path.resolve(__dirname, "..") +
      "\\video\\video-content\\thumbnail\\prelim-thumbnail"
  )
);

app.listen(3000, () => {
  console.log(`Server Started at ${3000}`);
});
