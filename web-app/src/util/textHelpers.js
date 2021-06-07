export function summarize(paragraphs) {
    let maxChars = 300
    let summary = ''
    for (let i = 0; i < paragraphs.length; i++) {
      const p = paragraphs[i]
      if (maxChars <= 0) {
        summary += '...'
        break
      }
      
      if (p.length > maxChars) {
        summary += p.substring(0, maxChars) + '...'
        break
      }

      summary += p
      maxChars -= p.length
    }

    return summary
}

export function concat(names) {
  let res = ''
  names.forEach((name, index) => {
    if (index < names.length - 1){
      res += name + ', '
    } else {
      res += name
    }
  });

  return res
}
