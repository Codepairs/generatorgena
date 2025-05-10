
import React, { useContext} from 'react';
import { Redirect, Route, Switch } from "react-router-dom";
import { privateRoutes, publicRoutes } from "../router";
import { AuthContext } from "../context";
import { BrowserRouter as Router } from 'react-router-dom';

const AppRouter = () => {
    const { isAuth, isLoading } = useContext(AuthContext);

    return (
        <div>
            {console.log(isAuth)}
        {
            <Router>
                <Switch>
                    {publicRoutes.map(route =>
                        <Route
                            component={route.component}
                            path={route.path}
                            exact={route.exact}
                            key={route.path}
                        />
                    )}
                    <Redirect to='/registration' />
                </Switch>
            </Router>
}
            </div>
            
    );
};

export default AppRouter;
