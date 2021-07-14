import _ from "lodash"
import primitives from "@primer/primitives"


const styles = {
    color: {
        bg: {
            header: primitives.colors.dark.header.bg,
            sider: primitives.colors.dark.scale.gray[7],
            menuItem: primitives.colors.dark.scale.gray[7],
            menuItemActive: primitives.colors.dark.scale.blue[6],
        },
        text: {
            header: primitives.colors.dark.header.text,
            sider: primitives.colors.dark.scale.gray[1],
            menuItemActive: primitives.colors.dark.scale.white,
        },
        border: {
            sider: primitives.colors.dark.scale.gray[0],
            menuItemActive: primitives.colors.dark.scale.blue[4],
        },
    },
    size: {
        height: {
            header: 64
        },
        width: {
            sider: {
                shrink: 64,
                expand: 150,
            }
        }
    }
}

// TODO 后续考虑使用 CSS var 实现可以动态调换
const styleGet = (name: string) => {
    return _.get(styles, name);
}
export default styleGet