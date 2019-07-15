import React from 'react';
import { shallow } from 'enzyme';
import render from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
  {
    'active': true,
    'email': 'mail1@mail.com',
    'id': 1,
    'username': 'mail1',
  },
  {
    'active': true,
    'email': 'mail2@mail.com',
    'id': 2,
    'username': 'mail2',
  },
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('mail1');
});

test('UsersList renders a snapshot properly', () => {
  const tree = render.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});