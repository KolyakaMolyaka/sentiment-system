/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     12.06.2024 15:40:13                          */
/*==============================================================*/


drop index MlModel_includes_Tokenizer_FK;

drop index MlModel_includes_Vectorization_;

drop index User_creates_MlModel_FK;

drop index MlModel_PK;

drop table MlModel;

drop index Tokenizer_PK;

drop table Tokenizer;

drop index User_PK;

drop table "User";

drop index Vectorization_PK;

drop table Vectorization;

/*==============================================================*/
/* Table: MlModel                                               */
/*==============================================================*/
create table MlModel (
   user_username        VARCHAR(128)         not null,
   ml_model_id          SERIAL               not null,
   tokenizer_title      VARCHAR(128)         not null,
   vectorization_title  VARCHAR(128)         not null,
   ml_model_title       VARCHAR(128)         not null,
   ml_model_accuracy    FLOAT8               null,
   ml_model_recall      FLOAT8               null,
   ml_model_precision   FLOAT8               null,
   ml_model_classifier  VARCHAR(128)         not null,
   ml_model_use_default_stop_words BOOL                 not null,
   ml_model_max_words   INT4                 not null,
   ml_model_min_token_length INT4                 not null,
   ml_model_delete_numbers_flag BOOL                 not null,
   ml_model_trained_self BOOL                 not null,
   constraint PK_MLMODEL primary key (user_username, ml_model_id)
);

/*==============================================================*/
/* Index: MlModel_PK                                            */
/*==============================================================*/
create unique index MlModel_PK on MlModel (
user_username,
ml_model_id
);

/*==============================================================*/
/* Index: User_creates_MlModel_FK                               */
/*==============================================================*/
create  index User_creates_MlModel_FK on MlModel (
user_username
);

/*==============================================================*/
/* Index: MlModel_includes_Vectorization_                       */
/*==============================================================*/
create  index MlModel_includes_Vectorization_ on MlModel (
vectorization_title
);

/*==============================================================*/
/* Index: MlModel_includes_Tokenizer_FK                         */
/*==============================================================*/
create  index MlModel_includes_Tokenizer_FK on MlModel (
tokenizer_title
);

/*==============================================================*/
/* Table: Tokenizer                                             */
/*==============================================================*/
create table Tokenizer (
   tokenizer_title      VARCHAR(128)         not null,
   tokenizer_description VARCHAR(1024)        not null,
   tokenizer_is_archived BOOL                 not null,
   constraint PK_TOKENIZER primary key (tokenizer_title)
);

/*==============================================================*/
/* Index: Tokenizer_PK                                          */
/*==============================================================*/
create unique index Tokenizer_PK on Tokenizer (
tokenizer_title
);

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   user_username        VARCHAR(128)         not null,
   user_password        VARCHAR(1024)        not null,
   constraint PK_USER primary key (user_username)
);

/*==============================================================*/
/* Index: User_PK                                               */
/*==============================================================*/
create unique index User_PK on "User" (
user_username
);

/*==============================================================*/
/* Table: Vectorization                                         */
/*==============================================================*/
create table Vectorization (
   vectorization_title  VARCHAR(128)         not null,
   vectorization_description VARCHAR(1024)        not null,
   vectorization_is_archived BOOL                 not null,
   constraint PK_VECTORIZATION primary key (vectorization_title)
);

/*==============================================================*/
/* Index: Vectorization_PK                                      */
/*==============================================================*/
create unique index Vectorization_PK on Vectorization (
vectorization_title
);

alter table MlModel
   add constraint FK_MLMODEL_MLMODEL_I_TOKENIZE foreign key (tokenizer_title)
      references Tokenizer (tokenizer_title)
      on delete restrict on update restrict;

alter table MlModel
   add constraint FK_MLMODEL_MLMODEL_I_VECTORIZ foreign key (vectorization_title)
      references Vectorization (vectorization_title)
      on delete restrict on update restrict;

alter table MlModel
   add constraint FK_MLMODEL_USER_CREA_USER foreign key (user_username)
      references "User" (user_username)
      on delete restrict on update restrict;

