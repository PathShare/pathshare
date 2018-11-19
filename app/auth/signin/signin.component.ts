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

  // closeResult: string;

  constructor(private modalService: NgbModal, private authService: AuthService, private _router: Router) {}

  openWindowCustomClass(content) {
    this.modalService.open(content, { windowClass: 'dark-modal' });
  }

  ngOnInit() {
  }

  onSignin(form: NgForm) {

    // userData: Json form of user's data
    const userData = JSON.stringify(form.value)
    this.authService.signinUser(userData)
      .subscribe(
        response => console.log("success",response),
        error => console.log("error", error)
      );

      this._router.navigate(['/'])
      

  }

}
