import React, { FC } from 'react';
import { Header } from '@/components/layout';
import AppContainer from '@/components/app-container';
import style from '@/App.module.css';
import { BrowserRouter as Router } from "react-router-dom";


const App: FC = () => (
    <div className={style.app}>
        <Router>
            <Header></Header>
            <div className={style['content-container']}>
                <AppContainer></AppContainer>
            </div>
        </Router>
    </div>
);

export default App;