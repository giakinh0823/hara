const Validator = (options) => {
    let getParent = (element, selector) => {
        while (element.parentElement) {
            if (element.parentElement.matches(selector)) {
                return element.parentElement;
            }
            element = element.parentElement
        }
    }
    let selectorRules = {}
    let validate = (inputElement, rule, errorElement) => {
        let errorMessage;
        let rules = selectorRules[rule.selector]

        for (let i = 0; i < rules.length; i++) {
            switch (inputElement.type) {
                case 'radio':
                case 'checkbox':
                    errorMessage = rules[i](
                        formElement.querySelector(rules.selector + ':checked')
                    )
                    break;
                default:
                    errorMessage = rules[i](inputElement.value)
            }
            if (errorMessage) break;
        }

        if (errorMessage) {
            errorElement.innerText = errorMessage
            errorElement.parentElement.classList.add('invalid')
            getParent(errorElement, options.formGroupSelector).classList.add('invalid')
        } else {
            errorElement.innerText = ''
            getParent(errorElement, options.formGroupSelector).classList.remove('invalid')
        }
        return !errorMessage
    }

    let formElement = document.querySelector(options.form);
    if (formElement) {
        formElement.onsubmit = (e) => {
            e.preventDefault();
            let isFormValid = true;
            options.rules.forEach((rule) => {
                let inputElement = formElement.querySelector(rule.selector)
                let errorElement = getParent(inputElement, options.formGroupSelector).querySelector(options.errorElement)
                let isValid = validate(inputElement, rule, errorElement)
                if (!isValid) {
                    isFormValid = false
                }
            })


            if (isFormValid) {
                if (typeof options.onSubmit === 'function') {
                    let enableInputs = formElement.querySelectorAll('[name]:not([disabled])')
                    let formValue = Array.from(enableInputs).reduce((value, input) => {
                        switch(input.type){
                            case 'radio':
                                value[input.name] = formElement.querySelector('input[name="'+input.name+'"]:checked').value
                                break;
                            case 'checkbox':
                                if(input.matches(':checked')){
                                    value[input.name] = ''
                                    return value;
                                }
                                if(!Array.isArray(value[input.name])){
                                    value[input.name] = []
                                }
                                value[input.name].push(input.value)
                                break;
                            case 'file':
                                value[input.name] = input.files
                                break;
                            default:
                                value[input.name] = input.value
                        }
                        return value
                    }, {})
                    options.onSubmit(formValue)
                } else {
                    formElement.submit()
                }
            }
        }
        options.rules.forEach((rule) => {
            if (Array.isArray(selectorRules[rule.selector])) {
                selectorRules[rule.selector].push(rule.test)
            } else {
                selectorRules[rule.selector] = [rule.test]
            }

            let inputElements = formElement.querySelectorAll(rule.selector)
            Array.from(inputElements).forEach((inputElement) => {
                let errorElement = getParent(inputElement, options.formGroupSelector).querySelector(options.errorElement)
                if (inputElement) {
                    inputElement.onblur = () => {
                        validate(inputElement, rule, errorElement)
                    }
                    inputElement.oninput = () => {
                        errorElement.innerText = ''
                        errorElement.parentElement.classList.remove('invalid')
                    }
                }
            })
        })
    }
}


Validator.isRequired = (selector, message) => {
    return {
        selector: selector,
        test: (value) => value ? undefined : message || 'Vui l??ng nh???p tr?????ng n??y'
    }
}

Validator.isEmail = (selector, message) => {
    return {
        selector: selector,
        test: (value) => {
            let regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
            return regex.test(value) ? undefined : message || 'Tr?????ng n??y ph???i l?? email'
        }
    }
}

Validator.minLength = (selector, min, message) => {
    return {
        selector: selector,
        test: (value) => {
            return value.length >= min ? undefined : message || `Vui l??ng nh???p t???i thi???u ${min} k?? t???`
        }
    }
}

Validator.isConfirmed = (selector, getConfirmValue, message) => {
    return {
        selector: selector,
        test: (value) => {
            return value === getConfirmValue() ? undefined : message || 'Gi?? tr??? nh???p v??o kh??ng ch??nh x??c'
        }
    }
}


