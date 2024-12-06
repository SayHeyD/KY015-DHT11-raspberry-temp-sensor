<?php

namespace App\Http\Controllers;

class IndexController extends Controller
{
    public function view() {
        return redirect()->route('dashboard');
    }
}
