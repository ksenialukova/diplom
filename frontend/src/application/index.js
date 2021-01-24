import React, { Component } from 'react'
import { Route, Switch } from 'react-router-dom'
import { withRouter } from 'react-router'

import Main from "./main"
import Upload from './upload'
import Reports from './analytics'

class Application extends Component {

    render() {
        return (
            <>
                <Switch>
                    <Route exact path='/' component={Main}/>
                    <Route path='/upload' component={Upload}/>
                    <Route path='/reports' component={Reports}/>
                </Switch>
            </>
        )
    }
}
export default withRouter(Application)
