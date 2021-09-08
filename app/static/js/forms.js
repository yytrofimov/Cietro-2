function validateEmail(forms) {
    let re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(forms.email.data).toLowerCase());
}

function validatePassword(forms) {
    let re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()+=-\?;,./{}|\":<>\[\]\\\' ~_]).{8,}/;
    return re.test(forms.password.data);
}

function validatePasswordRetype(forms) {
    if ((forms.password.data != null) & (forms.passwordretype.data != null)) {
        return forms.password.data == forms.passwordretype.data;
    } else {
        return false;
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function isNumeric(str) {
    if (!str) {
        return false;
    }
    return /^\d+$/.test(str);
}

function isAlNumeric(str) {
    if (!str) {
        return false;
    }
    return /^[a-z0-9]+$/i.test(str);
}

function validateFirstName(forms) {
    let regex = /^[a-zA-Z ]{2,30}$/;
    forms.firstname.data = capitalizeFirstLetter(forms.firstname.data);
    document.getElementById(forms.firstname.obj_id).value = forms.firstname.data;
    return regex.test(forms.firstname.data);
}

function validateLastName(forms) {
    let regex = /^[a-zA-Z ]{2,30}$/;
    forms.lastname.data = capitalizeFirstLetter(forms.lastname.data);
    document.getElementById(forms.lastname.obj_id).value = forms.lastname.data;
    return regex.test(forms.lastname.data);
}

function validateCompanyId(forms) {
    return !isNaN(parseFloat(forms.companyid.data)) && isFinite(forms.companyid.data);
}

function validateItemIdToActivate(forms) {
    return isNumeric(forms.itemidtoactivate.data);
}

function validateItemIdToDeactivate(forms) {
    return isNumeric(forms.itemidtodeactivate.data);
}
function validateItemIdToDelete(forms) {
    return isNumeric(forms.itemidtodelete.data);
}

function validateItemNameToAdd(forms) {
    return isAlNumeric(forms.itemnametoadd.data);
}

function validateActivationCode(forms) {
    return isAlNumeric(forms.activationcode.data);
}

function validateCompanyName(forms) {
    return isAlNumeric(forms.companyname.data);
}

function validateCompanyAddress(forms) {
    return isAlNumeric(forms.companyaddress.data);
}

function validateCompanyRegNumber(forms) {
    return isAlNumeric(forms.companyaddress.data);
}

function validateInviteCode(forms) {
    return isAlNumeric(forms.invitecode.data);
}

forms = {
    email: {
        obj_id: "inputEmail",
        val_funcs: [validateEmail],
        data: null,
        is_valid: false,
    },
    password: {
        obj_id: "inputPassword",
        val_funcs: [validatePassword],
        data: null,
        is_valid: false,
    },
    passwordretype: {
        obj_id: "inputPasswordRetype",
        val_funcs: [validatePassword, validatePasswordRetype],
        data: null,
        is_valid: false,
    },
    firstname: {
        obj_id: "inputFirstName",
        val_funcs: [validateFirstName],
        data: null,
        is_valid: false,
    },
    lastname: {
        obj_id: "inputLastName",
        val_funcs: [validateLastName],
        data: null,
        is_valid: false,
    },
    companyid: {
        obj_id: "inputCompanyId",
        val_funcs: [validateCompanyId],
        data: null,
        is_valid: false,
    },
    itemidtoactivate: {
        obj_id: "inputItemIdToActivate",
        val_funcs: [validateItemIdToActivate],
        data: null,
        is_valid: false,
    },
    itemidtodeactivate: {
        obj_id: "inputItemIdToDeactivate",
        val_funcs: [validateItemIdToDeactivate],
        data: null,
        is_valid: false,
    },
    itemidtodelete: {
        obj_id: "inputItemIdToDelete",
        val_funcs: [validateItemIdToDelete],
        data: null,
        is_valid: false,
    },
    itemnametoadd: {
        obj_id: "inputItemNameToAdd",
        val_funcs: [validateItemNameToAdd],
        data: null,
        is_valid: false,
    },
    activationcode: {
        obj_id: "inputActivationCode",
        val_funcs: [validateActivationCode],
        data: null,
        is_valid: false,
    },
    companyname: {
        obj_id: "inputCompanyName",
        val_funcs: [validateCompanyName],
        data: null,
        is_valid: false,
    },
    companyaddress: {
        obj_id: "inputCompanyAddress",
        val_funcs: [validateCompanyAddress],
        data: null,
        is_valid: false,
    },

    companyregnumber: {
        obj_id: "inputCompanyRegNumber",
        val_funcs: [validateCompanyRegNumber],
        data: null,
        is_valid: false,
    },
    invitecode: {
        obj_id: "inputInviteCode",
        val_funcs: [validateInviteCode],
        data: null,
        is_valid: false,
    },
};

buttons = {
    "register-button": [
        forms.email,
        forms.password,
        forms.passwordretype,
        forms.firstname,
        forms.lastname,
        forms.companyid,
    ],
    "login-button": [forms.email, forms.password],
    "company-register-button": [
        forms.email,
        forms.password,
        forms.passwordretype,
        forms.firstname,
        forms.lastname,
        forms.companyname,
        forms.companyaddress,
        forms.companyregnumber,
        forms.invitecode,
    ],
    "reset-password-button": [forms.password, forms.passwordretype],
    "forgot-password-button": [forms.email],
    "activate-item-button": [forms.activationcode, forms.itemidtoactivate],
    "deactivate-item-button": [forms.itemidtodeactivate],
    "delete-item-button": [forms.itemidtodelete],
    "add-item-button": [forms.itemnametoadd],
};

function make_handlers() {
    for (let button_id in buttons) {
        let button = document.getElementById(button_id);
        if (button) {
            for (let form_handler of buttons[button_id]) {
                let form = document.getElementById(form_handler.obj_id);
                if (form) {
                    form.addEventListener("input", function () {
                        let val_cond = true;
                        form_handler.data = form.value;
                        for (let val_func of form_handler.val_funcs) {
                            if (!val_func(forms)) {
                                val_cond = false;
                            }
                        }
                        form_handler.is_valid = val_cond;
                        console.log(forms);
                        unlock_button(button_id);
                    });
                } else {
                    form_handler.is_valid = true;
                }
            }
        }
    }
}

function unlock_button(button_id) {
    let val_conds = [];
    for (let form_handler of buttons[button_id]) {
        val_conds.push(form_handler.is_valid);
        var button_cond = val_conds.every((el) => {
            return el == true;
        });
    }
    let button = document.getElementById(button_id);
    if (button_cond) {
        if (button.hasAttribute("disabled")) {
            button.removeAttribute("disabled");
        }
    } else {
        if (!button.hasAttribute("disabled")) {
            button.setAttribute("disabled", "disabled");
        }
    }
}

make_handlers();
