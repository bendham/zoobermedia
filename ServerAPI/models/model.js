const mongoose = require("mongoose");

// const dataSchema = new mongoose.Schema({
//   name: {
//     required: true,
//     type: String,
//   },
//   age: {
//     required: true,
//     type: Number,
//   },
// });

// module.exports = mongoose.model("Data", dataSchema);

const VideoSchema = new mongoose.Schema({
  isMakingVideo: {
    required: true,
    type: Boolean,
  },
  dayOfWeek: {
    required: true,
    type: Number,
  },
  iscomment: {
    required: true,
    type: Boolean,
  },
  subreddit: {
    type: String,
  },
  numberOfClips: {
    type: Number,
  },
  videoNumber: {
    required: true,
    type: Number,
  },
  title: {
    required: true,
    type: String,
  },
  descrption: {
    required: true,
    type: String,
  },
  commentSubreddits: {
    type: [String],
  },
  clipsPerSub: {
    type: Number,
  },
});

const ProductionSchema = new mongoose.Schema({
  zooberType: {
    required: true,
    type: String,
  },
  currentDay: Number,
  videos: [VideoSchema],
  thumbnails: {
    type: [String],
  },
});

module.exports = mongoose.model("Data", ProductionSchema);
