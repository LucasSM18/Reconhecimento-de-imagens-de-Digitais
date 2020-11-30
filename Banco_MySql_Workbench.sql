Create database APS;
use APS;

Create Table Funcionarios(
CD_ID int primary key not null auto_increment,
NM_Funcionario varchar(30),
DS_Cargo varchar(20),
VL_Salario decimal(10,2),
IMG_Digital blob);

Create table Agrotoxicos(
CD_ID int primary key not null auto_increment,
NM_Agrotoxico varchar(20),
DS_Agrotoxico longtext
);

Create table propriedades(
ID_Propriedade int primary key not null auto_increment,
CD_IDAgrotoxicos int not null,
DS_Localização varchar(40),
DS_Propriedade longtext,
foreign key (CD_IDAgrotoxicos)
references Agrotoxicos(CD_ID)
);

Create table Ambiente(
CD_ID int primary key not null auto_increment,
CD_PropriedadeID int not null,
DS_Ambiente varchar(15),
DS_Descrição longtext,
foreign key (CD_PropriedadeID)
references propriedades(ID_Propriedade)
);


select * from funcionarios;




