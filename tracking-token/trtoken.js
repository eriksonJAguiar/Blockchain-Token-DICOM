const fs = require("fs")
const arrayOfFiles = fs.readdirSync("../../DICOM_TCIA/");
const path = require("path");
 
const getAllFiles = function(dirPath, arrayOfFiles) {
    try {
        files = fs.readdirSync(dirPath)
        
        arrayOfFiles = arrayOfFiles || []
        
        files.forEach(function(file) {
            if (fs.statSync(dirPath + "/" + file).isDirectory()) {
                arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles);
            } else {
                arrayOfFiles.push(path.join(__dirname, dirPath, "/", file));
                console.log(arrayOfFiles);
            }
        });
        return arrayOfFiles;
    } catch(e) {
        console.log(e);
    }
}



const main = function(){
    
}

main();
