import style from '@/App.module.css';
import Layout from '@/components/Layout';
import Main from '@/components/Main';
import { BrowserRouter as Router } from "react-router-dom";


const App = () => (
    <div className={ style.app }>
        <Router>
            <Layout.Header />
            <Main className={ style.main }/>
        </Router>
    </div>
);

export default App;