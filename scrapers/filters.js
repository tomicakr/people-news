function containsRegex(reg) {
    return function containsRegex(href) {
        return reg.test(href);
    }
}

function removeDuplicates(value, index, self){
    return self.indexOf(value) === index;
}

module.exports = {
    containsRegex,
    removeDuplicates
}
