import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import UsersList from 'components/UsersList';

class App extends Component {
  constructor (props) {
    super(props);

    this.state = {
      users: [],
    };
  }

  componentDidMount () {
    this._getUsers();
  }

  _getUsers () {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data.data.users });
      })
      .catch(error => {
        console.log(error);
      });
  }

  render () {
    return (
      <section className={'section'}>
        <div className="container">
          <div className="columns">
            <div className="column is-on-third">
              <br/>
              <h1 className="title is-1 is-1">All Users</h1>
              <hr/>
              <br/>
              <UsersList users={this.state.users}/>
            </div>
          </div>
        </div>
      </section>
    );
  }

}

ReactDOM.render(<App/>, document.getElementById('root'));