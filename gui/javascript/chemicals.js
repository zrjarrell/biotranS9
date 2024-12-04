import { getData, createTextedElement } from "./utilities.js";

const apiurl = "http://127.0.0.1:8000";
console.log("hello world");


///Result formatting

function buildPubchemCell(pubchemid) {
    let pubchemCell = document.createElement('a');
    pubchemCell.appendChild(document.createTextNode(pubchemid));
    pubchemCell.href = "https://pubchem.ncbi.nlm.nih.gov/compound/" + pubchemid;
    pubchemCell.target = "_blank";
    return pubchemCell
}



///Table building

function buildHead () {
    const header = document.createElement("button");
    header.id = "resultHead";
    header.appendChild(createTextedElement("p", "Name"));
    header.appendChild(createTextedElement("p", "Formula"));
    header.appendChild(createTextedElement("p", "Monoisotopic Mass"));
    header.appendChild(createTextedElement("p", "PubChemID"));
    return header
}

function makeResultRow(resultDict) {
    let row = document.createElement("button");
    row.classList.add('mainRow');
    row.id = resultDict['id'];
    row.appendChild(createTextedElement('p', resultDict['name'].replaceAll('_', ' ')));
    row.appendChild(createTextedElement('p', resultDict['formula']));
    row.appendChild(createTextedElement('p', resultDict['monoisotopic'].toFixed(4)));
    row.appendChild(buildPubchemCell(resultDict['pubchemid']));
    container.appendChild(row);
    container.appendChild(makeMinorRow(resultDict));
    row.addEventListener('click', function () {
        this.classList.toggle("active");
        console.log('clicked')
        var content = this.nextElementSibling;
        if (content.style.display === "grid") {
            content.style.display = "none";
        } else {
            content.style.display = "grid";
        }
    })
}

function makeMinorRow(resultDict) {
    let minorRow = document.createElement("div");
    minorRow.classList.add('minorRow');
    minorRow.id = '_' + resultDict['id'];
    let loading = document.createElement("img");
    let loadingDiv = document.createElement("div");
    loadingDiv.classList.add('loading');
    loading.src = "../assets/img/loader.gif";
    loadingDiv.appendChild(loading);
    minorRow.appendChild(loadingDiv);
    getData(apiurl + '/test/?id=' + resultDict['id']).then((result) => {
        loading.hidden = true;
        let chemicalImg = document.createElement("img");
        chemicalImg.src = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/" + resultDict['pubchemid'] + "/PNG";
        minorRow.appendChild(chemicalImg);
        let summaryDiv = document.createElement('div');
        summaryDiv.appendChild(createTextedElement('p', resultDict['smiles']));
        summaryDiv.appendChild(createTextedElement('p', ""));
        summaryDiv.appendChild(createTextedElement('p', "Total predicted metabolites: " + result['tot.predicted'].length));
        summaryDiv.appendChild(createTextedElement('p', "Number of detected metabolites: " + result['detected.metabolites'].length));
        summaryDiv.appendChild(createTextedElement('p', "Number of unique matching features: " + result['unique.feats.match'].length));
        minorRow.appendChild(summaryDiv);
        let detailButton = createTextedElement('button', "Detailed results");
        detailButton.value = resultDict['id'];
        minorRow.appendChild(detailButton)
    })
    minorRow.style.display = "none";
    return minorRow
}

function buildResults (result) {
    container.innerHTML = ""
    container.appendChild(buildHead())
    for(let i in result) {
        makeResultRow(result[i])
    }
}





///Functionality

const submit = document.getElementById('submit');
const searchtext = document.getElementById('searchtext');

const container = document.getElementById('container');

const rows = document.querySelectorAll('.mainrow');

submit.addEventListener('click', function () {
    console.log(apiurl)
    getData(apiurl + '/chemicals/?name=' + searchtext.value).then((result) => {
        buildResults(result)
    })
})

