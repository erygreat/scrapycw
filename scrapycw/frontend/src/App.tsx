import style from '@/App.module.css';
import { Header } from '@/components/layout';
import Main from '@/components/Main';
import { BrowserRouter as Router } from "react-router-dom";


const App = () => (
    <div className={ style.app }>
        <Router>
            <Header />
            <Main className={ style.main }/>
        </Router>
    </div>
);

export default App;