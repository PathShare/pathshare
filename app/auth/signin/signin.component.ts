import { UserDataService } from './../user-data.service';
import { User } from './../../shared/model/user';
import { AuthService } from './../auth.service';
import { NgForm } from '@angular/forms';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
//Kien: for popup
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class SigninComponent implements OnInit {

  hideSignInErrorMsg = true

  user: User

  constructor(private modalService: NgbModal, private authService: AuthService, private _router: Router, private _userDataService: UserDataService) {}

  openWindowCustomClass(content) {
    this.modalService.open(content, { windowClass: 'dark-modal' });
  }

  ngOnInit() {
  }

  ngOnAppear() {

  }

  onSignin(form: NgForm) {

    const formValue = form.value
    // getting user email from form
    const userEmail = formValue['email']

    this.authService.signinUser(userEmail)
      .subscribe(
        data => {
          this.user = data
          this._userDataService.updateUser(data['data'])
          this._router.navigate(['/'])
          this.modalService.dismissAll()
        },
        error => {
          console.log("error", error)
          this.hideSignInErrorMsg = false
        }
      );
  }


  reset() {
    this.hideSignInErrorMsg = true
  }

}
