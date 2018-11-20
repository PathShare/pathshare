import { User } from './../shared/model/user';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserDataService {

  constructor() { }

  user: User = {
    age: -1,
    email: "string",
    is_validated: false,
    major: "string",
    name: "string",
    password: "string",
    token: "string",
    username: "string",
    _id: "string"}

  // Update user information to the one on the info fetched from server
  updateUser(user: User) {
      this.user = user
  }

  public getUser() {
    return this.user
  }


}
