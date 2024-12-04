async function getData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        const json = await response.json()
        console.log(json);
        return json
    } catch (error) {
        console.log(error.message);
    }
}

function createTextedElement(type, text) {
    const elem = document.createElement(type);
    elem.appendChild(document.createTextNode(text));
    return elem;
}

export { getData, createTextedElement };