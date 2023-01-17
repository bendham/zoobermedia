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
