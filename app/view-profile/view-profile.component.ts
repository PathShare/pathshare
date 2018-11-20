import { User } from './../shared/model/user';
import { Component, OnInit } from '@angular/core';
import { UserDataService } from '../auth/user-data.service';

@Component({
  selector: 'app-view-profile',
  templateUrl: './view-profile.component.html',
  styleUrls: ['./view-profile.component.css']
})
export class ViewProfileComponent implements OnInit {

  user: User

  constructor(private userDataService: UserDataService) { }

  ngOnInit() {

  }


  update() {
    this.user = this.userDataService.getUser()
    console.log("TESTING:",this.user['name'])
  }

}
