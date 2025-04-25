
//import ChangeCode from "../pages/ChangeCode.jsx";
import ChangePass from "../pages/ChangePass.jsx";
//import CodeLight from "../pages/Light/CodeLight.jsx";
//import Links from "../pages/Links.jsx";
import Login from "../pages/Login.jsx";
import Main from "../pages/Main.jsx";
//import OurTeam from "../pages/OurTeam.jsx";
import Registration from "../pages/Registration.jsx";


export const privateRoutes = [
]

export const publicRoutes = [
  {path: '/login', component: Login, exact: true},
  {path: '/registration', component: Registration, exact: true},
    //{path: '/code', component: CodeLight, exact: true},
  {path: '/main', component: Main, exact: true},
    //{path: '/change-code', component: ChangeCode, exact: true},
    {path: '/change-pass', component: ChangePass, exact: true},
    //{path: '/ourteam', component: OurTeam, exact: true},
   // {path: '/links', component: Links, exact: true}
]
