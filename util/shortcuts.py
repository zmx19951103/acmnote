# -*- coding: utf-8 -*-
import os
from django.shortcuts import render


def error_page(request, error_reason):
    return render(request, "utils/error.html", {"error": error_reason})



