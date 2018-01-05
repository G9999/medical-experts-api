function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}
function getTop3Series(data){
    if(data.length <= 3)
        return data;

    var sorted = data.sort(dynamicSort("value"));
    var ret = [];
    ret.push(data[data.length -1]);
    ret.push(data[data.length -2]);
    ret.push(data[data.length -3]);
    return ret;
}
