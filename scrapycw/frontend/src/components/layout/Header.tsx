import GithubBtn from '@/components/common/GithubBtn';
import { Header as UIHeader } from '@ui';

const Header = () => (
    <UIHeader fixed height={ 40 }>
        <UIHeader.Item full>
        </UIHeader.Item>
        <UIHeader.Item>
            <GithubBtn size={ 16 }/>
        </UIHeader.Item>
    </UIHeader>
);

export default Header;