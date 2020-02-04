const fs = require("fs")
const arrayOfFiles = fs.readdirSync("../../DICOM_TCIA/");
const path = require("path");
const https = require('https');
const daikon = require('daikon');
//const dicom = require('dicom');
var dicom = require('dicom-parser');
const org = ['ICMC', 'Rib. USP', 'Poli USP', 'H. Albert Eistein', 'H. das Clinicas'];
const user_hprovider = ['user1', 'erikson','user2','user3', 'user4', 'user5'];
const user_research = ['ICMC', 'MIT', 'EACH', 'EESC', 'UENP'];
 
const getAllFiles = function(dirPath, arrayOfFiles) {
    try {
        files = fs.readdirSync(dirPath)
        
        arrayOfFiles = arrayOfFiles || []
        
        files.forEach(function(file) {
            if (fs.statSync(dirPath + "/" + file).isDirectory()) {
                arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles);
            } else {
                arrayOfFiles.push(path.join(__dirname, dirPath));
            }
        });
        return arrayOfFiles;
    } catch(e) {
        console.log(e);
    }
}

const print_dicom_element = function(json, elem) {
    console.log(dicom.json.get_value(json, elem));
};

const getDicomSeries = function(files){
    let dicom = files[0].split('/');
    f = [];
    dirs = []
    files.forEach(function(file){
        dir = file.split('/');
        if(dicom[dicom.length-2] === dir[dir.length-2]){
            f.push(file);
        }else{
            dicom = file.split('/');
            dirs.push(f);
            f = [];
        }
    });

    return dirs;
}

const registerDicom = function(pathfiles, org){
    pathfiles.forEach((path_) => {
        files = fs.readdirSync(path_);
        var image = null;
        var series = new daikon.Series();
        files.forEach((file) => {
            buf = fs.readFileSync(path.join(path_,file));
            image = daikon.Series.parseImage(new DataView(daikon.Utils.toArrayBuffer(buf)));
            if (image === null) {
                console.error(daikon.Series.parserError);
            } else if (image.hasPixelData()) {
                if ((series.images.length === 0) || (image.getSeriesId() === series.images[0].getSeriesId())) {
                    series.addImage(image);
                }
            }
        });
        series.buildSeries();
    });

    return series;
}

const shareDicom = function(files){
   return 0;
}


const main = function(){
    
    const files = getAllFiles("../../DICOM_TCIA/");
    var unique = files.slice(4).filter((v, i, a) => a.indexOf(v) === i); 
    //registerDicom(unique);
    var dataSet = dicom.parseDicom(dicomFileAsBuffer);

}

main();
