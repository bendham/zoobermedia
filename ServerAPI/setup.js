require("dotenv").config();

const mongoose = require("mongoose");
const ZooberModel = require("./models/model");
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

function defaultVideo(dayOfWeek) {
  this.isMakingVideo = true;
  this.dayOfWeek = dayOfWeek;
  this.iscomment = true;
  this.subreddit = "contagiouslaughter";
  this.numberOfClips = 50;
  this.videoNumber = 10;
  this.title = "Contagious Laughter Compilation";
  this.descrption = "Fun Video";
  this.commentSubreddits = ["rafasf", "sdfsdg", "sdgjjfgj"];
  this.clipsPerSub = 10;
}

const zoober = new ZooberModel({
  zooberType: "main",
  currentDay: 0,
  videos: [
    new defaultVideo(0),
    new defaultVideo(1),
    new defaultVideo(2),
    new defaultVideo(3),
    new defaultVideo(4),
    new defaultVideo(5),
    new defaultVideo(6),
  ],
  thumbnails: Array(3).fill(
    "https://www.readersdigest.ca/wp-content/uploads/2017/10/funny-photos-llama.jpg"
  ),
});

zoober.save((err, zoo) => {
  if (err) return console.error(err);

  // This will print inserted record from database
  console.log(zoo);
});
