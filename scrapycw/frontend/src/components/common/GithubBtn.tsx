import { GithubOutlined } from '@ant-design/icons';
import config from "@/config";

interface GithubBtnProps {
    size?: number
}

const GithubBtn = (props: GithubBtnProps) => {
    const goGithub = () => {
        window.open(config.github);
    }
    return <GithubOutlined style={{ fontSize: props.size || 14 + 'px' }} onClick={ () => goGithub()} />
}

export default GithubBtn