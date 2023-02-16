<template>
    <header>
        <nav class="navbar is-primary">
            <div class="navbar-brand">
                <a class="navbar-item" href="../">
                    <img src="@/assets/logo-hor.png" />
                </a>
            </div>
            <div class="navbar-end">
                <a class="navbar-item">Sign In</a>
                <a class="navbar-item">Sign Up</a>
                <div class="navbar-item has-dropdown is-hoverable d">
                    <a class="navbar-item">
                        <span>
                            <font-awesome-icon icon="fa-solid fa-user" />
                        </span>
                    </a>
                    <div class="navbar-dropdown is-boxed is-right">
                        <a class="navbar-item">Profile</a>
                        <a class="navbar-item">Notes</a>
                        <a class="navbar-item">Setting</a>
                        <a class="navbar-item">Log Out</a>
                    </div>
                </div>
                <!-- <UserDropDownButton /> -->
            </div>
        </nav>
    </header>
</template>
