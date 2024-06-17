
# Table of Contents

1.  [RichSpot](#org0b141a4)
    1.  [Ncspot discord rich presence add-on](#org5e7e59d)
    1.  [Assets Notice](#org5e7e592)
    2.  [Installing / Running RichSpot](#org14af663)
        1.  [Through PyPi](#org1cd60f9)
        2.  [Manually](#org6ef52cc)
        3.  [Running](#org597ff1a)
    3.  [Requirements](#orgfa35322)
        1.  [How to obtain client id and authorization token?](#org5997f48)
        2.  [WARNING ⚠](#org6cef86a)


<a id="org0b141a4"></a>

# RichSpot

<a id="org5e7e59d"></a>

## [Ncspot](https://github.com/hrkfdn/ncspot) discord rich presence add-on

Since **ncspot** doesn&rsquo;t implement spotify connect, we cannot share our listening activity in discord&rsquo;s rich presence.
Thus using **RichSpot** makes it possible to do.

![img](https://raw.githubusercontent.com/M1ndo/RichSpot/main/imgs/example.png)


<a id="org14af663"></a>

## Assets Notice
Assets will not be visible until they're cached this is a limitation of =discord=.
It will take atleast 10-15 min before they're visible.

## Installing / Running RichSpot


<a id="org1cd60f9"></a>

### Through PyPi

``` shell
pip install richspot
```

<a id="org6ef52cc"></a>

### Manually

``` shell
pip install -r requirements.txt
pip install . --user
```

<a id="org597ff1a"></a>

### Running

``` shell
richspot & # Run in the background
```

<a id="orgfa35322"></a>

## Requirements


<a id="org5997f48"></a>

### How to obtain client id and authorization token?

- Go to discord developers [page](https://discord.com/developers/applications/).
- Create an application with a custom name.
- Get **application id** in generation info tab.
- Optionally upload a cover image for rich presence invite.

**Authorization Token** is used to upload and delete song cover assets.

- Open developers tools (Inspect Elements) (F12)

![img](https://raw.githubusercontent.com/M1ndo/RichSpot/main/imgs/auth_token.png)


<a id="org6cef86a"></a>

### WARNING ⚠

Do not share any keys with anyone unless you want to lose your account.

