function formatMktCp(num) {
    if (num >= 1000000000000) {//1T
        num = Math.round(num / 10000000000)/100
        return `${num}T`
    }
    else if (num >= 1000000000) {//1B
        num = Math.round(num / 10000000)/100
        return `${num}B`
    }
    else if (num >= 1000000) {//1M
        num = Math.round(num / 1000000)/100
        return `${num}M`}
    else {
        return `${num}`
    }}
    
export default formatMktCp;