/**
 * 解析命令行参数，参考：https://github.com/gcc-mirror/gcc/blob/master/libiberty/argv.c
 * 
 * nodeJS和python底层都是使用的C的库，即这里面的方法
 */
const argv = (command: string): Array<string> =>  {
    const regPattern = /[ |'|"|\v|\r|\n|\r|\t|\\]/;
    const results = [];
    let text = '';
    let index = command.search(regPattern);

    while(index >= 0) {
        let subText = command.slice(0, index);
        text += subText;
        command = command.slice(index);

        let matchText = '';
        let matchTextGroups = command.match(regPattern);
        if(matchTextGroups && matchTextGroups.length > 0) {
            matchText = matchTextGroups[0];
        } else {
            throw new Error("正则匹配失败！");
        }
        if(matchText === '\\') {
            text += command.slice(0, matchText.length + 1);
            command = command.slice(matchText.length + 1);
        } else if(['\'', '"'].indexOf(matchText) >= 0) {
            command = command.slice(matchText.length);
            var dIndex = command.search(matchText);
            if(dIndex < 0) {
                throw new Error('没有闭合标签: [' + matchText + ']');
            } else {
                text += command.slice(0, dIndex);
                command = command.slice(dIndex + matchText.length);
            }
        } else if([' ', '\v', '\r', '\n', '\r', '\t'].indexOf(matchText) >= 0) {
            command = command.slice(matchText.length);
            if(text) {
                results.push(text);
            }
            text = '';
        }
        index = command.search(regPattern);
    }
    text += command;
    if(text) {
        results.push(text);
    }
    return results;
}
export default argv;

export const verify = (text: string, pattern: string) => {
    const results = argv(text);
    for(let i = 0; i < results.length; i++) {
        let result = results[i];
        if(i % 2 === 0 && result !== pattern) {
            throw new Error("格式错误");
        }
    }
    if(results.length % 2 !== 0) {
        throw new Error("格式错误");
    }
}

export const format = (text: string) => {
    const texts = argv(text);
    let result = "";
    texts.forEach((_text: string) => {
        if(_text.search(" ") >= 0) {
            result += JSON.stringify(_text) + " ";
        } else {
            result += _text + " ";
        }
    })
    if(result.length > 0) {
        result = result.slice(0, result.length - 1);
    }
    return result;
}

export const group = (text: string, pattern: string) => {
    try {
        verify(text, pattern);
        const texts = argv(text);
        const results = {};
        texts.forEach(text => {
            if(text !== pattern) {
                let index = text.search("=")
                let key = text.slice(0, index);
                let value = text.slice(index + 1);
                console.log(key, value);
                results[key] = value;
            }
        });
        return results;
    } catch(e) {
        return null;
    }
}