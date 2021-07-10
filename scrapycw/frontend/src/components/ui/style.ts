import _ from "lodash"

const styles = {
    color: {
        bg: {
            header: "#001529",
        },
        text: {
            header: "#ffffffd9"
        }
    },
    size: {
        height: {
            header: 64
        },
    }
}

const styleGet = (name: string) => {
    return _.get(styles, name);
}
export default styleGet