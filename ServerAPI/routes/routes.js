const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
// const Model = require("../models/model");
const router = express.Router();

const Model = require("../models/model");

//Post Method
// router.post("/post", async (req, res) => {
//   const data = new Model({
//     name: req.body.name,
//     age: req.body.age,
//   });

//   try {
//     const dataToSave = await data.save();
//     res.status(200).json(dataToSave);
//   } catch (error) {
//     res.status(400).json({ message: error.message });
//   }
// });

// //Get all Method
// router.get("/getAll", async (req, res) => {
//   try {
//     const data = await Model.find();
//     res.json(data);
//   } catch (error) {
//     res.status(500).json({ message: error.message });
//   }
// });

// //Get by ID Method
// router.get("/getOne/:id", async (req, res) => {
//   try {
//     const data = await Model.findById(req.params.id);
//     res.json(data);
//   } catch (error) {
//     res.status(500).json({ message: error.message });
//   }
// });

// //Update by ID Method
// router.patch("/update/:id", async (req, res) => {
//   try {
//     const id = req.params.id;
//     const updatedData = req.body;
//     const options = { new: true };

//     const result = await Model.findByIdAndUpdate(id, updatedData, options);

//     res.send(result);
//   } catch (error) {
//     res.status(400).json({ message: error.message });
//   }
// });

// //Delete by ID Method
// router.delete("/delete/:id", async (req, res) => {
//   try {
//     const id = req.params.id;
//     const data = await Model.findByIdAndDelete(id);
//     res.send(`Document with ${data.name} has been deleted...`);
//   } catch (error) {
//     res.status(400).json({ message: error.message });
//   }
// });

// Make total new Zoober entry
router.post("/post", async (req, res) => {
  const data = new Model({
    name: req.body.name,
    age: req.body.age,
  });

  try {
    const dataToSave = await data.save();
    res.status(200).json(dataToSave);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

//Get all Method
router.get("/getAll", async (req, res) => {
  try {
    const data = await Model.find();
    res.json(data);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

//Get all Method
router.get("/", async (req, res) => {
  try {
    res.json("API works :)");
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// // Get images
// router.get("/getImages", async (req, res) => {
//   try {
//     var files = fs.readdirSync("/images/");
//   } catch (error) {
//     res.status(500).json({ message: error.message });
//   }
// });

//Get by ID Method
router.get("/getOne/:id", async (req, res) => {
  try {
    const data = await Model.findById(req.params.id);
    res.json(data);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

//Update by ID Method
router.patch("/update", async (req, res) => {
  try {
    const updatedData = req.body;
    const options = { new: true };

    const result = await Model.updateOne(
      { zooberType: "main" },
      updatedData,
      options
    );

    res.send(result);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.post("/makevideo", async (req, res) => {
  try {
    // const updatedData = req.body;
    // const options = { new: true };
    console.log("Making video!");
    const python = spawn("python", [
      path.resolve(__dirname, "..", "..", "MakeVideo.py"),
      JSON.stringify(req.body),
    ]);

    python.stdout.on("data", function (data) {
      console.log(data.toString());
    });

    python.stderr.on("data", function (data) {
      console.error(data.toString());
    });

    res.status(200).json({ message: "video being made made!" });

    // res.send(req.body);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

//Delete by ID Method
router.delete("/delete/:id", async (req, res) => {
  try {
    const id = req.params.id;
    const data = await Model.findByIdAndDelete(id);
    res.send(`Document with ${data.name} has been deleted...`);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

module.exports = router;
