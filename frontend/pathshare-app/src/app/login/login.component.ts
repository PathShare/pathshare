import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }
  public dialogOpened = false;
  public windowOpened = false;

    public close(component) {
      this[component + 'Opened'] = false;
    }

    public open(component) {
      this[component + 'Opened'] = true;
    }

    public action(status) {
      console.log(`Dialog result: ${status}`);
      this.dialogOpened = false;
    }
}
