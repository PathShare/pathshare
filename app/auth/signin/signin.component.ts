import { AuthService } from './../auth.service';
import { NgForm } from '@angular/forms';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
//Kien: for popup
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class SigninComponent implements OnInit {

  // closeResult: string;

  constructor(private modalService: NgbModal, private authService: AuthService) {}

  openWindowCustomClass(content) {
    this.modalService.open(content, { windowClass: 'dark-modal' });
  }

  ngOnInit() {
  }

  onSignin(form: NgForm) {
    const email = form.value.email;
    const password = form.value.password;
    this.authService.signinUser(email,password);
  }

}
